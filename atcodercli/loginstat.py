"""
This module is used to get your current login status
"""

from .get_session import get_session
from rich.console import Console
import re

def handle(console: Console):
    console.log("getting login status...")
    session = get_session(console)
    res = session.get("https://atcoder.jp")
    if res.status_code == 200:
        try:
            username = re.findall(r'var userScreenName = "(\S+)";', res.text)[0]
            console.log(f"[green]successfully logged in as user {username}[/green]")
        except IndexError:
            console.log("[red]FATAL:failed to login[/red]")
            raise SystemExit(1)
    else:
        console.log("[red]FATAL:failed to login[/red]")
        raise SystemExit(1)

