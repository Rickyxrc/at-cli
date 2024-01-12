"""
This module is used to watch a page of records of a contest until judge ends
"""

import re
from rich.console import Console
from bs4 import BeautifulSoup
from ..utils.get_session import get_session
from .watchresult import watch_result

def handle(console: Console, arg):
    """
    handle args
    """
    contest_id = arg.contest_id
    session = get_session(console)
    res = session.get(f"https://atcoder.jp/contests/{contest_id}/submissions")
    doc = BeautifulSoup(res.text, features="html.parser")
    lis = [ int(t) for t in re.findall(r"/submissions/(\d+)", str(doc)) ]
    watch_result(console, contest_id, lis)
