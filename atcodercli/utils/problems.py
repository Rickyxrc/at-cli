"""
This module is used to load problem.yaml
"""

from bs4.element import whitespace_re
from rich.console import Console
import yaml
import os
import pathlib

class ProblemSet:
    def __init__(self, file_path:pathlib.Path, console:Console) -> None:
        self.filePath = file_path
        self.dat = yaml.safe_load(open(file_path, "r", encoding = "utf-8"))
        self.console = console
        console.log("adding", file_path)
    def add_problem(self, contest_id:str, problem_id:str) -> None:
        addobj = {"contest_id": contest_id, "problem_id": problem_id, "accepted": False}
        if not addobj in self.dat['problems']:
            self.dat['problems'].append(addobj)
        else:
            self.console.log(f"[yellow]problem {contest_id} {problem_id} already exists.[/yellow]")
    def save(self) -> None:
        with open(self.filePath, "w", encoding = "utf-8") as write_stream:
            write_stream.write(yaml.safe_dump(self.dat))

def tryLoadProblem(pathStr:str, console:Console) -> ProblemSet:
    """
    Try to load problem.yaml from all subdirs.
    If not found, throw Error
    """
    path = pathlib.Path(pathStr)
    while True:
        if (path / "problem.yaml") .exists():
            return ProblemSet(path / "problem.yaml", console)
        if path == pathlib.Path('/'):
            console.log("[red]No problem.yaml found.[/red]")
            console.log("You may want to start a contest using 'atcli contest race'")
            console.log("create one manually using 'atcli problem init'")
            raise SystemExit(1)
        console.log(f"\"problem.yaml\" not found in {path}, searching up")
        path = path.parent

