"""
This module is used to fetch a page of records of a contest until judge ends
"""

from rich.console import Console
from rich.progress import Progress
from .get_session import get_session
from .fetchresult import fetch_result
from time import sleep
from bs4 import BeautifulSoup
import re

def handle(console: Console):
    contest_id = "abc335"
    session = get_session(console)
    res = session.get(f"https://atcoder.jp/contests/{contest_id}/submissions")
    # print(res.text)
    doc = BeautifulSoup(res.text, features="html.parser")
    lis = [ int(t) for t in re.findall(r"/submissions/(\d+)", str(doc)) ]
    fetch_result(console, contest_id, lis)
    # print(doc.select(".table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(7)"))
    # print(doc)

