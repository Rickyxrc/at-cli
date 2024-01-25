"""
This module is used to watch a page of records of a contest until judge ends
"""

import re

import requests
from bs4 import BeautifulSoup
from rich.console import Console

from ..utils.get_session import get_session
from .watch_result import watch_result


def get_list(url: str, session: requests.Session) -> list[int]:
    """
    Read a submission result page and return a list of ids.
    """
    res = session.get(url)
    doc = BeautifulSoup(res.text, features="html.parser")
    lis = [int(t) for t in re.findall(r"/submissions/(\d+)", str(doc))]
    return lis


def handle(console: Console, arg):
    """
    Entry of cli, handle args.
    """
    contest_id = arg.contest_id
    session = get_session(console)
    watch_result(
        console,
        contest_id,
        get_list(f"https://atcoder.jp/contests/{contest_id}/submissions", session),
    )
