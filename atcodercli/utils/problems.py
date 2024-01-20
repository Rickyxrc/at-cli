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
            self.console.log(f"[yellow]problem {contest_id} {problem_id} already exists.[/yellow]")
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

def tryLoadProblemDirectly(pathStr: str, console: Console):
    """
        Try to load problem.yaml from path
        If not found, throw Error
    """
    path = pathlib.Path(pathStr)
    if (path / "problem.yaml").exists():
        return ProblemSet(path / "problem.yaml", console)
    else:
        console.log(f"[red]file {path / 'problem.yaml'} not exist.[/red]")
        console.log("You may want to start a contest using 'atcli contest race'")
        console.log("create one manually using 'atcli problem init'")
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
            console.log(f"[red]No problem.yaml found under {pathStr}.[/red]")
            console.log("You may want to start a contest using 'atcli contest race'")
            console.log("create one manually using 'atcli problem init'")
            raise SystemExit(1)
        console.log(f"\"problem.yaml\" not found in {path}, searching up")
        path = path.parent

