"""
    Init a contest
    Pull all samples, generate sample file.
"""
import os
import pathlib

from bs4 import BeautifulSoup
from rich.console import Console

from atcodercli.utils.config import Config

from ..utils.get_session import get_session
from .add_problem import add_problem
from .init_problem import init


def handle(console: Console, arg):
    """
    Entry of cli, handle args.
    """
    config = Config(console)
    path = pathlib.Path(os.getcwd())
    init(console, path, arg.force)
    session = get_session(console)
    endpoint = f"https://atcoder.jp/contests/{arg.contest_id}/tasks"
    res = session.get(endpoint)
    html = BeautifulSoup(res.text, features="html.parser")
    template = (
        arg.template if arg.template is not None else config.dat["template"]["default"]
    )
    for problem in list(html.select("td.text-center.no-break")):
        if not "Submit" in problem.a.string:
            problem_id = problem.a["href"].split("_")[-1]
            add_problem(
                path,
                console,
                arg.contest_id,
                problem_id,
                arg.force,
                template,
                config,
                f"{arg.contest_id}_{problem_id}",
            )
