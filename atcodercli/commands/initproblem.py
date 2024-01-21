from rich.console import Console
import yaml
import os
import pathlib

def init(console, filepath:str|pathlib.Path, force:bool):
    path = pathlib.Path(filepath)
    if (path / "problem.yaml").exists() and not force:
        console.print("[red]" + _("problem.yaml already exists under %s") % path + "[/red]")
        console.print(_("to override, use --force"))
        raise SystemExit(1)
    with open(path / "problem.yaml", "w", encoding = "utf-8") as write_stream:
        write_stream.write("problems: []")
    console.print(_("initialized empty problem.yaml, now use \"atcli problem add\""))

def handle(console:Console, arg):
    init(console, os.getcwd(), arg.force)

