from rich.console import Console
from .initproblem import init
from .addproblem import add_problem
from ..utils.get_session import get_session
import os
from bs4 import BeautifulSoup

def handle(console:Console, arg):
    init(console, os.getcwd(), arg.force)
    session = get_session(console)
    endpoint = f"https://atcoder.jp/contests/{arg.contest_id}/tasks"
    res = session.get(endpoint)
    html = BeautifulSoup(res.text, features="html.parser")
    for problem in list(html.select("td.text-center.no-break")):
        if not "Submit" in problem.a.string:
            problemId = problem.a['href'].split("_")[-1]
            add_problem(console, arg.contest_id, problemId)
