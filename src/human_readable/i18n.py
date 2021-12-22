"""Activate, get and deactivate translations."""
from __future__ import annotations

import gettext as gettext_module
import os.path
import sys
import threading


__all__ = ["activate", "deactivate", "gettext", "ngettext"]

_TRANSLATIONS = {"": gettext_module.NullTranslations()}
_CURRENT = threading.local()


def _get_default_locale_path() -> str | None:
    try:
        if not __file__:
            return None
        return os.path.join(os.path.dirname(__file__), "locale")
    except NameError:
        return None


def get_translation() -> gettext_module.NullTranslations:
    try:
        return _TRANSLATIONS[_CURRENT.locale]
    except (AttributeError, KeyError):
        return _TRANSLATIONS[""]


def activate(locale: str, path: str | None = None) -> gettext_module.NullTranslations:
    """Activate internationalisation.

    Set `locale` as current locale. Search for locale in directory `path`.

    Args:
        locale: Language name, e.g. `en_GB`.
        path: Path to search for locales.

    Returns:
        dict: Translations.

    Raises:
        Exception: If human readable cannot find the locale folder.
    """
    if path is None:
        path = _get_default_locale_path()

    if path is None:
        raise Exception(
            "Human readable cannot determinate the default location of the 'locale' "
            "folder. You need to pass the path explicitly."
        )
    if locale not in _TRANSLATIONS:
        translation = gettext_module.translation("human_readable", path, [locale])
        _TRANSLATIONS[locale] = translation
    _CURRENT.locale = locale
    return _TRANSLATIONS[locale]


def deactivate() -> None:
    """Deactivate internationalisation."""
    _CURRENT.locale = None


def gettext(message: str) -> str:
    """Get translation.

    Args:
        message: Text to translate.

    Returns:
        Translated text.
    """
    return get_translation().gettext(message)


def pgettext(msgctxt: str, message: str) -> str:
    """Fetches a particular translation.

    It works with `msgctxt` .po modifiers and allows duplicate keys with different
    translations.

    Args:
        msgctxt: Context of the translation.
        message: Text to translate.

    Returns:
        Translated text.
    """
    # This GNU gettext function was added in Python 3.8, so for older versions we
    # reimplement it. It works by joining `msgctx` and `message` by '4' byte.
    # Python 3.8+
    if sys.version_info >= (3, 8):
        return get_translation().pgettext(msgctxt, message)
    # Python 3.7 and older
    else:
        key = msgctxt + "\x04" + message
        translation = get_translation().gettext(key)
        return message if translation == key else translation


def ngettext(message: str, plural: str, num: int) -> str:
    """Plural version of gettext.

    Args:
        message: Singular text to translate.
        plural: Plural text to translate.
        num: The number (e.g. item count) to determine translation for the
            respective grammatical number.

    Returns:
        Translated text.
    """
    return get_translation().ngettext(message, plural, num)


def gettext_noop(message: str) -> str:
    """Mark a string as a translation string without translating it.

    Example usage:
        >>> CONSTANTS = [gettext_noop('first'), gettext_noop('second')]
        ... def num_name(n):
        ...    return gettext(CONSTANTS[n])

    Args:
        message: Text to translate in the future.

    Returns:
        Original text, unchanged.
    """
    return message
