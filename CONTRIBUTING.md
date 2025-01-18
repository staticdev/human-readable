# Contributor Guide

Thank you for your interest in improving this project.
This project is open-source under the [MIT license] and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code]
- [Documentation]
- [Issue Tracker]
- [Code of Conduct]

[mit license]: https://opensource.org/licenses/MIT
[source code]: https://github.com/staticdev/human-readable
[documentation]: https://human-readable.readthedocs.io/
[issue tracker]: https://github.com/staticdev/human-readable/issues

## How to report a bug

Report bugs on the [Issue Tracker].

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

## How to request a feature

Request features on the [Issue Tracker].

## How to set up your development environment

You need Python 3.9+ and the following tools:

- [UV]

Install the package with development requirements:

```sh
$ uv sync --all-extras --frozen
```

[uv]: https://docs.astral.sh/uv/

## How to test the project

Run the full test suite:

```sh
$ uv run nox
```

You can run a specific Nox session.
For example, invoke the unit test suite like this:

```sh
$ uv run nox -s tests
```

Unit tests are located in the `tests` directory,
and are written using the [pytest] testing framework.

## How to add a new locale

Make sure you have installed a PO Editor, you can easily install that on a Debian-based system with:

```sh
apt install poedit
```

To add a new locale you need to execute:

```sh
xgettext --from-code=UTF-8 -o human_readable.pot -k'_' -k'N_' -k'P_:1c,2' -l python src/human_readable/*.py  # extract new phrases
msginit -i human_readable.pot -o human_readable/locale/<locale name>/LC_MESSAGES/human_readable.po --locale <locale name>
```

Then edit your .po file in the locale folder that got created.

If possible, add tests to `tests/functional/new_locale`. Run them with:

```sh
nox -s tests
```

## How to submit changes

Open a [pull request] to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks before commiting your change, you can install pre-commit as a Git hook by running the following command:

```sh
$ nox --session=pre-commit -- install
```

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

[pull request]: https://github.com/staticdev/human-readable/pulls
[pytest]: https://pytest.readthedocs.io/

<!-- github-only -->

[code of conduct]: CODE_OF_CONDUCT.md

## How to release a new version

Just push a tag starting with v and using semantic versioning. Eg.

```sh
git tag v2.0.0
git push --tags
```
