"""
    This module is used to load problem.yaml
"""
import pathlib

from rich.console import Console
import yaml

class ProblemNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ProblemSet:
    def __init__(self, file_path:pathlib.Path, console:Console) -> None:
        self.filePath = file_path
        self.dat = yaml.safe_load(open(file_path, "r", encoding = "utf-8"))
        self.console = console
    def add_problem(self, contest_id:str, problem_id:str) -> None:
        addobj = {"contest_id": contest_id, "problem_id": problem_id, "accepted": False, "templates": []}
        if not addobj in self.dat['problems']:
            self.dat['problems'].append(addobj)
        else:
            self.console.print(f"[yellow]problem {contest_id} {problem_id} already exists.[/yellow]")
    def add_template(self, contest_id:str, problem_id:str, file_path:str, template:str) -> None:
        addobj = {"path": file_path, "template": template}
        for index, problem in enumerate(self.dat['problems']):
            if problem['contest_id'] == contest_id and problem['problem_id'] == problem_id:
                if addobj not in self.dat['problems'][index]['templates']:
                    self.dat['problems'][index]['templates'].append(addobj)
                return
        raise ProblemNotFoundError
    def save(self) -> None:
        with open(self.filePath, "w", encoding = "utf-8") as write_stream:
            write_stream.write(yaml.safe_dump(self.dat))

def tryLoadProblemInProblem(pathStr: str, console: Console):
    """
        Load problem.yaml exactly from parent
        if not found, throw Error
        if not found but problem.yaml exist on $pwd, give user hints.
    """
    path = pathlib.Path(pathStr)
    if (path.parent / "problem.yaml").exists():
        return ProblemSet(path.parent / "problem.yaml", console)
    else:
        if (path / "problem.yaml").exists():
            console.print("[red]" + _("This command should run under problem dir, not contest's root dir.") + "[/red]")
            console.print(_("please cd in problem dir and exec this command again!"))
        console.print("[red]" + _("problem.yaml not found in parent dir.") + "[/red]")
        raise SystemExit(1)

def tryLoadProblemDirectly(pathStr: str, console: Console):
    """
        Try to load problem.yaml from path
        If not found, throw Error
    """
    path = pathlib.Path(pathStr)
    if (path / "problem.yaml").exists():
        return ProblemSet(path / "problem.yaml", console)
    else:
        console.print("[red]" + _("file %s not exist.") % (path / 'problem.yaml') + "[/red]")
        console.print(_("You may want to start a contest using 'atcli contest race'"))
        console.print(_("create one manually using 'atcli problem init'"))
        raise SystemExit(1)

def tryLoadProblem(pathStr:str, console:Console) -> ProblemSet:
    """
        Try to load problem.yaml from all parents.
        If not found, throw Error
    """
    path = pathlib.Path(pathStr)
    while True:
        if (path / "problem.yaml").exists():
            return ProblemSet(path / "problem.yaml", console)
        if path == pathlib.Path('/'):
            console.print("[red]" + _("No problem.yaml found under %s.") % path + "[/red]")
            console.print(_("You may want to start a contest using 'atcli contest race'"))
            console.print(_("create one manually using 'atcli problem init'"))
            raise SystemExit(1)
        console.print(_("\"problem.yaml\" not found in %s, searching up") % path)
        path = path.parent

def getProblemName(pathStr:str, problems:ProblemSet, console:Console):
    """
        Get Problem by path and problem object from parent
        like: getProblemName(
            "/home/ricky/oi/abc000/abc000_a",
            tryLoadProblemDirectly("/home/ricky/oi/abc000", console),
            console
        ) = ("abc000", "a")
    """
    path = pathlib.Path(pathStr)
    try:
        contest_id, problem_id = path.name.split("_")
    except ValueError:
        console.print("[red]" + _("%s invalid, don't look like <contest_id>_<problem_id>") % path + "[/red]")
        console.print(_("use \"atcli problem add\" or \"atcli contest race\", cd in that dir and execute this command again!"))
        raise SystemExit(1)
    exist = False
    for problem in problems.dat['problems']:
        if problem['contest_id'] == contest_id and problem['problem_id'] == problem_id:
            exist = True
    if not exist:
        console.print("[red]" + _("problem %s not exist") % (path.name) + "[/red]")
        console.print("[blue]" + _("tip: don't create problem dir manually, use \"atcli problem add\" or \"atcli contest race\"") + "[/blue]")
        raise SystemExit(1)
    return (contest_id, problem_id)

