import pathlib
from rich.console import Console

from atcodercli.commands.inittemplate import initFile
from atcodercli.utils.config import Config
from atcodercli.utils.problems import tryLoadProblemDirectly
from .initproblem import init
from .addproblem import add_problem
from ..utils.get_session import get_session
import os
from bs4 import BeautifulSoup

def handle(console:Console, arg):
    config = Config(console)
    path = pathlib.Path(os.getcwd())
    init(console, path, arg.force)
    session = get_session(console)
    endpoint = f"https://atcoder.jp/contests/{arg.contest_id}/tasks"
    res = session.get(endpoint)
    html = BeautifulSoup(res.text, features="html.parser")
    for problem in list(html.select("td.text-center.no-break")):
        if not "Submit" in problem.a.string:
            problemId = problem.a['href'].split("_")[-1]
            add_problem(console, arg.contest_id, problemId)
    problemObject = tryLoadProblemDirectly(path, console)
    if arg.template == None:
        template_name:str = config.dat['template']['default']
    else:
        template_name:str = arg.template
    for problem in problemObject.dat['problems']:
        initFile(
            path / f"{arg.contest_id}_{problem['problem_id']}" / f"{arg.contest_id}_{problem['problem_id']}",
            config.dat['template']['default'],
            config,
            problemObject,
            problem['contest_id'],
            problem['problem_id'],
            arg.force,
            console,
        )
