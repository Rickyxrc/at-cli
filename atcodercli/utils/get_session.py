"""
This helper function is used to load session file at ~/.config/atcli/session.yaml
"""
import os
import re

import requests
import yaml
from requests.utils import cookiejar_from_dict, dict_from_cookiejar
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
    session.headers.update(
        {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
        }
    )
    return session


def get_csrf(
    session: requests.Session, _console: Console, url: str = "https://atcoder.jp"
) -> str:
    """
    Get session
    """
    request_result = session.get(url)
    return re.findall(r'var csrfToken = "(\S+)"', request_result.text)[0]


def save_session(console: Console, session: requests.Session) -> None:
    """
    Save session to ~/.config/atcli/session.yaml
    """
    conf = yaml.safe_dump({"cookies": dict_from_cookiejar(session.cookies)})

    home = os.path.expanduser("~")
    if not os.path.exists(os.path.join(home, ".config")):
        console.print(_("creating dir %s") % os.path.join(home, ".config"))
        os.mkdir(os.path.join(home, ".config"))
    if not os.path.exists(os.path.join(home, ".config", "atcli")):
        console.print(_("creating dir %s") % os.path.join(home, ".config", "atcli"))
        os.mkdir(os.path.join(home, ".config", "atcli"))
    with open(
        os.path.join(home, ".config", "atcli", "session.yaml"),
        "w",
        encoding="utf-8",
    ) as write_stream:
        write_stream.write(conf)


if __name__ == "__main__":
    session_get = get_session(Console())
    USERNAME = "ricky_awa"
    res = session_get.get("https://atcoder.jp")
    print(USERNAME in res.text)  # True
