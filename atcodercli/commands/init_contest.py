import os
import pathlib

from bs4 import BeautifulSoup
from rich.console import Console

from atcodercli.commands.init_template import init_file
from atcodercli.utils.config import Config
from atcodercli.utils.problems import load_problem_directly

from ..utils.get_session import get_session
from .add_problem import add_problem
from .init_problem import init


def handle(console: Console, arg):
    config = Config(console)
    path = pathlib.Path(os.getcwd())
    init(console, path, arg.force)
    session = get_session(console)
    endpoint = f"https://atcoder.jp/contests/{arg.contest_id}/tasks"
    res = session.get(endpoint)
    html = BeautifulSoup(res.text, features="html.parser")
    for problem in list(html.select("td.text-center.no-break")):
        if not "Submit" in problem.a.string:
            problem_id = problem.a["href"].split("_")[-1]
            add_problem(console, arg.contest_id, problem_id)
    problem_object = load_problem_directly(path, console)
    template_name: str = (
        config.dat["template"]["default"] if arg.template is None else arg.template
    )
    for problem in problem_object.dat["problems"]:
        init_file(
            path
            / f"{arg.contest_id}_{problem['problem_id']}"
            / f"{arg.contest_id}_{problem['problem_id']}",
            template_name,
            config,
            problem_object,
            problem["contest_id"],
            problem["problem_id"],
            arg.force,
            console,
        )
