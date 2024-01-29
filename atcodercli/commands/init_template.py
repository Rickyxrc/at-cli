"""
This module is used to init code from a template.
"""
import os
import pathlib

from rich.console import Console

from ..utils.config import Config
from ..utils.problems import ProblemSet, get_problem_name, load_parent_of_problem


def init_file(
    path: str,
    template: str,
    config: Config,
    problems: ProblemSet,
    contest_id: str,
    problem_id: str,
    force: bool,
    console: Console,
):
    """
    Init a file with a template.
    """
    template_path = pathlib.Path(
        os.path.expanduser(config.dat["template"]["types"][template]["file"])
    )
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as read_stream:
            code_template = read_stream.read()
        console.print(_('loaded template "%s" from %s') % (template, template_path))
    else:
        console.print(
            "[red]"
            + _('template "%s" file %s does not exist!') % (template, template_path)
            + "[/red]"
        )
        raise SystemExit(1)
    generate_file = str(path) + f".{config.dat['template']['types'][template]['ext']}"
    if pathlib.Path(generate_file).exists() and not force:
        console.print("[red]" + _("file %s already exists!") % generate_file + "[/red]")
        console.print(_("to override, use --force"))
        console.print(_("or if you want to create other file, use --name <file_name>"))
        raise SystemExit(1)
    with open(generate_file, "w", encoding="utf-8") as write_stream:
        write_stream.write(code_template)
        console.print(_("generated %s") % generate_file)
    problems.add_template(contest_id, problem_id, generate_file, template)
    problems.save()


def handle(console: Console, arg):
    """
    Entry of cli, handle args.
    """
    path = pathlib.Path(os.getcwd())
    problems = load_parent_of_problem(path, console)
    contest_id, problem_id = get_problem_name(path, problems, console)
    config = Config(console)
    file_name = path.name if arg.name is None else arg.name
    template = config.dat["template"]["default"]
    init_file(
        path / file_name,
        template,
        config,
        problems,
        contest_id,
        problem_id,
        arg.force,
        console,
    )
