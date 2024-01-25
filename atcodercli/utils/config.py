"""
This module is used to load ~/.config/atcli/config.yaml
"""

import os
import pathlib

import yaml
from rich.console import Console


def _check_path(dic: dict, path: str, origin: str, console: Console):
    """
    For the ducumention, please refer to check_path, this function is the inner function.
    """
    if not isinstance(dic, dict):
        console.print(
            "[red]"
            + _("Incorrect type in config path %s, expect dict, found %s")
            % (origin, str(type(dic)))
            + "[/red]"
        )
        raise SystemExit(1)
    if "." in path:
        var = path.split(".")[0]
        path_remain = ".".join(path.split(".")[1:])
        subdic = dic.get(var)
        if subdic is None:
            console.print(
                "[red]" + _("config %s not exist in config.yaml.") % (origin) + "[/red]"
            )
            raise SystemExit(1)
        return _check_path(subdic, path_remain, origin, console)

    if dic.get(path) is None:
        console.print(
            "[red]" + _("config %s not exist in config.yaml.") % (origin) + "[/red]"
        )
        raise SystemExit(1)
    return dic.get(path)


# TODO: Fix this dirty solution.
def check_path(dic: dict, path: str, console: Console):
    """
    Input a dict and dot seprated path.
    Try get the path from dict
    If failed, raise systemExit
    If succeed, return value
    """
    return _check_path(dic, path, path, console)


def check_template(dic: dict, name: str, console: Console):
    """
    Check if a template defined in config is valid.
    """
    base_path = f"template.types.{name}"
    check_path(dic, f"{base_path}.file", console)
    check_path(dic, f"{base_path}.lang_id", console)
    check_path(dic, f"{base_path}.ext", console)
    check_path(dic, f"{base_path}.test", console)
    check_path(dic, f"{base_path}.test.before", console)
    check_path(dic, f"{base_path}.test.run", console)
    check_path(dic, f"{base_path}.test.after", console)


def check_differ(dic: dict, name: str, console: Console):
    """
    Check if a checker defined in config is valid.
    """
    base_path = f"checker.types.{name}"
    check_path(dic, f"{base_path}", console)


class Config:
    """
    Config is a read-only object now (cannot write to dir)
    """

    def __init__(self, console: Console) -> None:
        self.config_path = (
            pathlib.Path(os.path.expanduser("~")) / ".config/atcli/config.yaml"
        )
        if not self.config_path.exists():
            console.print(
                "[yellow]"
                + _("No config file found under ~/.config/atcli/config.yaml")
                + "[/yellow]"
            )
            with open(self.config_path, "w", encoding="utf-8") as write_stream:
                write_stream.write("")
            console.print(_("created a null config at %s") % self.config_path)
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.dat = yaml.safe_load(f)
        self.console = console

        template_default = check_path(self.dat, "template.default", console)
        check_path(self.dat, f"template.types.{template_default}", console)
        for template in check_path(self.dat, "template.types", console).keys():
            check_template(self.dat, template, console)
        checker_default = check_path(self.dat, "checker.default", console)
        check_path(self.dat, f"checker.types.{checker_default}", console)
        for checker in check_path(self.dat, "checker.types", console).keys():
            check_differ(self.dat, checker, console)


if __name__ == "__main__":
    conf = Config(Console())
