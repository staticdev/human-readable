"""Nox sessions."""

import os
import shlex
import shutil
import sys
from pathlib import Path
from textwrap import dedent

import nox


package = "human_readable"
python_versions = ["3.13", "3.12", "3.11", "3.10", "3.9"]
nox.needs_version = ">= 2024.10.9"
nox.options.default_venv_backend = "uv"
nox.options.sessions = (
    "pre-commit",
    "mypy",
    "tests",
    "typeguard",
    "xdoctest",
    "docs-build",
)


def activate_virtualenv_in_precommit_hooks(session: nox.Session) -> None:
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the
    session's virtual environment. This allows pre-commit to locate hooks in
    that environment when invoked from git.

    Args:
        session: The Session object.

    """
    assert session.bin is not None  # noqa: S101

    # Only patch hooks containing a reference to this session's bindir. Support
    # quoting rules for Python and bash, but strip the outermost quotes so we
    # can detect paths within the bindir, like <bindir>/python.
    bindirs = [
        bindir[1:-1] if bindir[0] in "'\"" else bindir
        for bindir in (repr(session.bin), shlex.quote(session.bin))
    ]

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    headers = {
        # pre-commit < 2.16.0
        "python": f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """,
        # pre-commit >= 2.16.0
        "bash": f"""\
            VIRTUAL_ENV={shlex.quote(virtualenv)}
            PATH={shlex.quote(session.bin)}"{os.pathsep}$PATH"
            """,
    }

    hookdir = Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    for hook in hookdir.iterdir():
        if hook.name.endswith(".sample") or not hook.is_file():
            continue

        if not hook.read_bytes().startswith(b"#!"):
            continue

        text = hook.read_text()

        if not any(
            Path("A") == Path("a")
            and bindir.lower() in text.lower()
            or bindir in text
            for bindir in bindirs
        ):
            continue

        lines = text.splitlines()

        for executable, header in headers.items():
            if executable in lines[0].lower():
                lines.insert(1, dedent(header))
                hook.write_text("\n".join(lines))
                break


@nox.session(name="pre-commit", python=python_versions[0])
def precommit(session: nox.Session) -> None:
    """Lint using pre-commit."""
    args = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]
    session.install(
        "pre-commit",
        "pre-commit-hooks",
        "ruff",
    )
    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)


@nox.session(python=python_versions)
def mypy(session: nox.Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or ["src", "tests", "docs/conf.py"]
    session.install(".")
    session.install("mypy", "freezegun", "pytest")
    session.run("mypy", *args)
    if not session.posargs:
        session.run(
            "mypy", f"--python-executable={sys.executable}", "noxfile.py"
        )


@nox.session(python=python_versions)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install(
        "coverage[toml]", "pytest", "pytest_mock", "pygments", "freezegun"
    )
    try:
        session.run(
            "coverage", "run", "--parallel", "-m", "pytest", *session.posargs
        )
    finally:
        if session.interactive:
            session.notify("coverage")


@nox.session(python=python_versions[0])
def coverage(session: nox.Session) -> None:
    """Produce the coverage report."""
    # Do not use session.posargs unless this is the only session.
    nsessions = len(session._runner.manifest)
    has_args = session.posargs and nsessions == 1
    args = session.posargs if has_args else ["report"]
    session.install("coverage[toml]")
    if not has_args and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")
    session.run("coverage", *args)


@nox.session(python=python_versions[0])
def typeguard(session: nox.Session) -> None:
    """Runtime type checking using Typeguard."""
    session.install(".")
    session.install(
        "pytest", "pytest_mock", "freezegun", "typeguard", "pygments"
    )
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)


@nox.session(python=python_versions)
def xdoctest(session: nox.Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.install(".")
    session.install("xdoctest[colors]")
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(name="docs-build", python=python_versions[0])
def docs_build(session: nox.Session) -> None:
    """Build the documentation."""
    # args = session.posargs or [
    #     "-b",
    #     "linkcheck",
    #     "-W",
    #     "--keep-going",
    #     "docs",
    #     "docs/_build",
    # ]
    args = session.posargs or ["docs", "docs/_build"]
    if not session.posargs and "FORCE_COLOR" in os.environ:
        args.insert(0, "--color")

    # session.install(".")
    session.install("sphinx", "furo", "myst-parser")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)


@nox.session(python=python_versions[0])
def docs(session: nox.Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    # session.install(".")
    session.install("sphinx", "sphinx-autobuild", "furo", "myst-parser")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)
