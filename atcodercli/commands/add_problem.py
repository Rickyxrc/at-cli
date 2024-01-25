"""
This module is used to add the problem to your current problem.yaml
"""

import os
import pathlib
import re

from bs4 import BeautifulSoup
from rich.console import Console

from atcodercli.commands.init_template import init_file

from ..utils.config import Config
from ..utils.get_session import get_session
from ..utils.problems import load_problem_from_all_ancestors


def add_problem(
    path: pathlib.Path,
    console: Console,
    contest_id: str,
    problem_id: str,
    force: bool,
    template: str,
    config: Config,
    file_name: str,
):
    """
    Add a problem to ./problem.yaml
    """
    problems = load_problem_from_all_ancestors(path, console)
    while not (path / "problem.yaml").exists():
        path = path.parent
    session = get_session(console)
    console.print(_("Adding problem %s...") % (f"{contest_id}_{problem_id}"))
    endpoint = (
        f"https://atcoder.jp/contests/{contest_id}/tasks/{contest_id}_{problem_id}"
    )
    res = session.get(endpoint)
    html = BeautifulSoup(res.text, features="html.parser")
    base_dir = problems.file_path.parent
    for sample in list(html.select(".part>section")):
        stat_str = sample.h3
        foldername = f"{contest_id}_{problem_id}"
        if not (base_dir / foldername).exists():
            os.mkdir(base_dir / foldername)
        try:
            if "Sample Input" in stat_str.string:
                sample_id = int(re.findall("Sample Input (\\d+)", stat_str.string)[0])
                code_block = sample.pre.string
                with open(
                    base_dir / f"{contest_id}_{problem_id}" / f"{sample_id}.in",
                    "w",
                    encoding="utf-8",
                ) as write_stream:
                    write_stream.write(code_block)
            if "Sample Output" in stat_str.string:
                sample_id = int(re.findall("Sample Output (\\d+)", stat_str.string)[0])
                code_block = sample.pre.string
                with open(
                    base_dir / f"{contest_id}_{problem_id}" / f"{sample_id}.ans",
                    "w",
                    encoding="utf-8",
                ) as write_stream:
                    write_stream.write(code_block)
        except IndexError:
            console.print(
                "[red]"
                + _("Failed when parsing %s.") % (f"{contest_id}_{problem_id}")
                + "[/red]"
            )
            console.print(_("This problem maybe a [bold]interactive problem[/bold]."))
            console.print(
                _(
                    "If not, this behavior might not net your expectation, please open a issue and let me know."
                )
            )
    problems.add_problem(contest_id, problem_id)
    problems.save()
    console.print(
        "[green]"
        + _("success fully add problem %s") % (f"{contest_id}_{problem_id}")
        + "[/green]"
    )
    init_file(
        path / f"{contest_id}_{problem_id}" / file_name,
        template,
        config,
        problems,
        contest_id,
        problem_id,
        force,
        console,
    )


def handle(console: Console, arg):
    """
    Entry of cli, handle args.
    """
    config = Config(console)
    template = (
        arg.template if arg.template is not None else config.dat["template"]["default"]
    )
    file_name = (
        arg.name if arg.name is not None else f"{arg.contest_id}_{arg.problem_id}"
    )
    add_problem(
        pathlib.Path(os.getcwd()),
        console,
        arg.contest_id,
        arg.problem_id,
        arg.force,
        template,
        Config(console),
        file_name,
    )
