"""
This module is used to get your current login status
"""

import re

from rich.console import Console

from ..utils.get_session import get_session


def handle(console: Console, _arg):
    """
    Entry of cli, handle args.
    """
    console.print(_("getting login status..."))
    session = get_session(console)
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
