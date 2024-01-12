"""
This module is used to get your current login status
"""

import re
from rich.console import Console
from ..utils.get_session import get_session

def handle(console: Console, arg):
    """
    handle args
    """
    console.log("getting login status...")
    session = get_session(console)
    res = session.get("https://atcoder.jp")
    if res.status_code == 200:
        try:
            username = re.findall(r'var userScreenName = "(\S+)";', res.text)[0]
            console.log(f"[green]successfully logged in as user {username}[/green]")
        except IndexError as exc:
            console.log("[red]FATAL:failed to login[/red]")
            raise SystemExit(1) from exc
    else:
        console.log("[red]FATAL:failed to login[/red]")
        raise SystemExit(1)
