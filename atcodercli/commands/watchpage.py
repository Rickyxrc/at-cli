"""
This module is used to fetch a page of records of a contest until judge ends
"""

from rich.console import Console
from utils.get_session import get_session
from .watchresult import fetch_result
from bs4 import BeautifulSoup
import re

def handle(console: Console, arg):
    contest_id = arg.contest_id
    session = get_session(console)
    res = session.get(f"https://atcoder.jp/contests/{contest_id}/submissions")
    doc = BeautifulSoup(res.text, features="html.parser")
    lis = [ int(t) for t in re.findall(r"/submissions/(\d+)", str(doc)) ]
    fetch_result(console, contest_id, lis)

