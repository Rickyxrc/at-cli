import gettext, pathlib, rich

LOCALEDIR = pathlib.Path(__file__).parent / "locales"
gettext.install("atcodercli", localedir=LOCALEDIR)

