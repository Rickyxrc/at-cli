"""
This module is used to init a null problem.yaml
"""
import os
import pathlib

from rich.console import Console


def init(console: Console, filepath: pathlib.Path, force: bool):
    """
    Init a empty problem.yaml.
    Args:
        filepath(pathlib.Path):
        force(bool): will override exist problem.yaml if set to True, otherwise not.
        console(Console):
    Returns:
        None
    """
    path = pathlib.Path(filepath)
    if (path / "problem.yaml").exists() and not force:
        console.print(
            "[red]" + _("problem.yaml already exists under %s") % path + "[/red]"
        )
        console.print(_("to override, use --force"))
        raise SystemExit(1)
    with open(path / "problem.yaml", "w", encoding="utf-8") as write_stream:
        write_stream.write("problems: []")
    console.print(_('initialized empty problem.yaml, now use "atcli problem add"'))


def handle(console: Console, arg):
    """
    Entry of cli, handle args.
    """
    init(console, os.getcwd(), arg.force)
