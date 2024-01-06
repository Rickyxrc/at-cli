"""
This module is used to login user and save session at ~/.config/atcli/session.yaml
TODO: Add override confirm;
"""

import requests, re
import os
from rich.console import Console
from bs4 import BeautifulSoup
# from utils.confirm import confirm
import yaml
from requests.utils import dict_from_cookiejar

def handle(console: Console):
    console.log("logging in...")

    username = console.input("username:")
    password = console.input("password(invisible):", password=True)

    session = requests.session()

    res = session.get("https://atcoder.jp/")
    csrf = re.findall(r'var csrfToken = "(\S+)"', res.text)[0]

    res = session.post("https://atcoder.jp/login",
        data = {
            "username": username,
            "password": password,
            "csrf_token": csrf
        },
    )

    if res.status_code == 403:
        console.log("[red]FATAL: blocked by atcoder.[/red]")
    
    doc = BeautifulSoup(res.text, features = "html.parser")
    if "Username or Password is incorrect" in str(doc.select("div.alert")):
        console.log("[red]ERROR: Username or Password is incorrect[/red]")
    elif username in str(res.text):
        console.log(f"[green]welcome, user {username}.[/green]")
        # if confirm(console, "save password?"):
        # TODO : save password for auto flush(optional)
        conf = yaml.safe_dump({
            'cookies': dict_from_cookiejar(session.cookies),
            'username': username
        })
        home = os.path.expanduser("~")
        if not os.path.exists(os.path.join(home, ".config")):
            console.log(f'creating dir \"{os.path.join(home, ".config")}\"')
            os.mkdir(os.path.join(home, ".config"))
        if not os.path.exists(os.path.join(home, ".config", "atcli")):
            console.log(f'creating dir \"{os.path.join(home, ".config", "atcli")}\"')
            os.mkdir(os.path.join(home, ".config", "atcli"))
        with open(os.path.join(home, ".config", "atcli", "session.yaml"), "w", encoding = "utf-8") as write_stream:
            write_stream.write(conf)
    else:
        console.log(doc)
        console.log("[red]ERROR: unhandled statment[/red]")

