"""
    Load gettext function _() to translate
"""
import gettext
import locale
import pathlib

LOCALEDIR = pathlib.Path(__file__).parent / "locales"

LANG = locale.getdefaultlocale()[0]

if LANG is None:
    LANG = "en_US"

try:
    lang = gettext.translation(
        "atcodercli",
        languages=[
            LANG,
        ],
        localedir=LOCALEDIR,
    )
    lang.install()
except FileNotFoundError:
    gettext.install("atcodercli")
