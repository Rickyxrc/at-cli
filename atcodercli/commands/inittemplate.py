import pathlib
from rich.console import Console
from ..utils.config import Config
from ..utils.problems import tryLoadProblemDirectly, ProblemSet
import os

def initFile(path: str, template: str, config: Config, problems: ProblemSet, console: Console, contest_id:str, problem_id:str, force:bool):
    template_path = pathlib.Path(os.path.expanduser(config.dat['template']['types'][template]['file']))
    if template_path.exists():
        with open(template_path, "r", encoding = "utf-8") as read_stream:
            code_template = read_stream.read()
        console.log(f"loaded template \"{template}\" from {template_path}")
    else:
        console.log(f"[red]template \"{template}\" file {template_path} does not exist![/red]")
        raise SystemExit(1)
    generate_file = str(path) + f".{config.dat['template']['types'][template]['ext']}"
    if pathlib.Path(generate_file).exists() and not force:
        console.log(f"[red]file {generate_file} already exists![/red]")
        console.log("use --force to override")
        raise SystemExit(1)
    with open(generate_file, "w", encoding = "utf-8") as write_stream:
        write_stream.write(code_template)
        console.log(f"generated {generate_file}")
    problems.add_template(contest_id, problem_id, generate_file, template)
    problems.save()

def handle(console:Console, arg):
    path = pathlib.Path(os.getcwd())
    # console.log(path.name)
    problems = tryLoadProblemDirectly(path.parent, console)
    try:
        contest_id, problem_id = path.name.split("_")
    except ValueError:
        console.log(f"[red]{path} invalid, don't look like <contest_id>_<problem_id>[/red]")
        console.log("use \"atcli problem add\" or \"atcli contest race\", cd in that dir and execute this command again!")
        raise SystemExit(1)
    config = Config(console)
    exist = False
    for problem in problems.dat['problems']:
        if problem['contest_id'] == contest_id and problem['problem_id'] == problem_id:
            exist = True
    if not exist:
        console.log(f"[red]problem {path.name} not exist[/red]")
        console.log("[blue]tip: don't create problem dir manually, use \"atcli problem add\" or \"atcli contest race\"[/blue]")
        raise SystemExit(1)
    file_name = path.name if arg.name is None else arg.name
    template = config.dat['template']['default']
    initFile(path / file_name, template, config, problems, console, contest_id, problem_id, arg.force)

