from rich.console import Console
import yaml
import os
import pathlib

def handle(console:Console, arg):
    path = pathlib.Path(os.getcwd())
    if (path / "problem.yaml").exists() and not arg.force:
        console.log(f"[red]problem.yaml already exists under {path}[/red]")
        console.log(f"to override, use --force")
        raise SystemExit(1)
    with open(path / "problem.yaml", "w", encoding = "utf-8") as write_stream:
        write_stream.write("problems: []")
    console.log("initialized empty problem.yaml, now use \"atcli problem add\"")

