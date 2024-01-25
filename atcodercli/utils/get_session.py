"""
This helper function is used to load session file at ~/.config/atcli/session.yaml
"""
import os
import re

import requests
import yaml
from requests.utils import cookiejar_from_dict
from rich.console import Console


def get_session(console: Console) -> requests.Session:
    """
    read the file ~/.config/atcli/session.yaml, and
    return a requests.session object
    """
    try:
        with open(
            os.path.join(os.path.expanduser("~"), ".config", "atcli", "session.yaml"),
            encoding="utf-8",
        ) as read_stream:
            dat = yaml.safe_load(read_stream)
    except FileNotFoundError as exc:
        console.print(
            "[red]"
            + _("ERROR:no session file found at %s")
            % os.path.join(os.path.expanduser("~"), ".config", "atcli", "config.yaml")
            + "[/red]"
        )
        console.print(_('try run "atcli login" first.'))
        raise SystemExit(1) from exc
    session = requests.session()
    session.cookies.update(cookiejar_from_dict(dat["cookies"]))
    return session


def get_csrf(
    session: requests.Session, _console: Console, url: str = "https://atcoder.jp"
) -> str:
    """
    Get session
    """
    request_result = session.get(url)
    return re.findall(r'var csrfToken = "(\S+)"', request_result.text)[0]


if __name__ == "__main__":
    session_get = get_session(Console())
    USERNAME = "ricky_awa"
    res = session_get.get("https://atcoder.jp")
    print(USERNAME in res.text)  # True
