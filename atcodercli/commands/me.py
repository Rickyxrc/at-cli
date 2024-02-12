"""
This module is used to get your current login status
"""

import re

import requests
from rich.console import Console


def handle(console: Console, session: requests.Session):
    """
    Entry of cli, handle args.
    """
    console.print(_("getting login status..."))
    res = session.get("https://atcoder.jp")
    if res.status_code == 200:
        try:
            username = re.findall(r'var userScreenName = "(\S+)";', res.text)[0]
            console.print(
                "[green]"
                + _("successfully logged in as user %s") % username
                + "[/green]"
            )
        except IndexError as exc:
            console.print("[red]" + _("FATAL:failed to login") + "[/red]")
            raise SystemExit(1) from exc
    else:
        console.print("[red]" + _("FATAL:failed to login") + "[/red]")
        raise SystemExit(1)
