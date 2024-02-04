"""
    Load gettext function _() to translate
"""
import gettext
import locale
import os
import pathlib

LOCALEDIR = pathlib.Path(__file__).parent / "locales"

LANG = None

if LANG is None:
    LANG = os.environ["LANG"]

if LANG is None:
    # pylint: disable=deprecated-method
    LANG = locale.getdefaultlocale()[0]

if LANG is None:
    LANG = "en_US"

if LANG == "en_US":
    gettext.install("atcodercli")
else:
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
        print(f"WARN: language {LANG} not found.")
        print(f"localedir = {LOCALEDIR}")
        gettext.install("atcodercli")
