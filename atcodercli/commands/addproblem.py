"""
This module is used to add the problem to your current problem.yaml
"""

import rich
from rich.console import Console
from ..utils.problems import tryLoadProblem
import os
import re
import pathlib
from ..utils.get_session import get_session
from bs4 import BeautifulSoup

def add_problem(console:Console, contest_id:str, problem_id:str):
    problems = tryLoadProblem(os.getcwd(), console)
    session = get_session(console)
    console.print(_("add problem %s_%s") % (contest_id, problem_id))
    endpoint = f"https://atcoder.jp/contests/{contest_id}/tasks/{contest_id}_{problem_id}"
    res = session.get(endpoint)
    html = BeautifulSoup(res.text, features="html.parser")
    base_dir = problems.filePath.parent
    for sample in list(html.select(".part>section")):
        stat_str = sample.h3
        foldername = f"{contest_id}_{problem_id}"
        if not (base_dir / foldername).exists():
            os.mkdir(base_dir / foldername)
        if 'Sample Input' in stat_str.string:
            id = int(re.findall("Sample Input (\d+)", stat_str.string)[0])
            code_block = sample.pre.string
            with open(base_dir / f"{contest_id}_{problem_id}" / f"{id}.in", "w", encoding = "utf-8") as write_stream:
                write_stream.write(code_block)
        if 'Sample Output' in stat_str.string:
            id = int(re.findall("Sample Output (\d+)", stat_str.string)[0])
            code_block = sample.pre.string
            with open(base_dir / f"{contest_id}_{problem_id}" / f"{id}.ans", "w", encoding = "utf-8") as write_stream:
                write_stream.write(code_block)
    problems.add_problem(contest_id, problem_id)
    problems.save()

def handle(console:Console, arg):
    """
    handle args
    """
    add_problem(console, arg.contest_id, arg.problem_id)
