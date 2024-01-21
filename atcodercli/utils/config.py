"""
This module is used to load ~/.config/atcli/config.yaml
"""

from rich.console import Console
import yaml
import os
import pathlib

class Config:
    """
        Config is a read-only object now(cannot write to dir)
    """
    def __init__(self, console:Console) -> None:
        self.config_path = pathlib.Path(os.path.expanduser("~")) / ".config/atcli/config.yaml"
        if not self.config_path.exists():
            console.print("[yellow]No config file found under ~/.config/atcli/config.yaml[/yellow]")
            with open(self.config_path, "w", encoding = "utf-8") as write_stream:
                write_stream.write("")
            console.print(f"created a null config {self.config_path}")
        self.dat = yaml.safe_load(open(self.config_path, "r", encoding = "utf-8"))
        self.console = console

