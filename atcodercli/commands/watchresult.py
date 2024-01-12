"""
This module is used to fetch a result of records until judge ends
You needn't to call it most of time
"""

from rich.console import Console
from rich.progress import Progress
from utils.get_session import get_session
from time import sleep
import re

def render_status(stat:str) -> str:
    return {
        "Judging": "[gray]Judging[/gray]",
        "Accepted": "[green]Accepted[/green]",
        "Time Limit Exceeded": "[yellow]Time Limit Exceeded[/yellow]",
        "Runtime Error": "[yellow]Runtime Error[/yellow]",
        "Compilation Error": "[yellow]Compilation Error[/yellow]",
        "Wrong Answer": "[yellow]Wrong Answer[/yellow]",
        "Not Found": "Not Found"
    }.get(
        stat,
        f"Unknown status {stat}"
    )

def fetch_result(console:Console, contest_id:str, sids:list):
    with Progress(console=console) as progress:
        console.log(f"Fetching result with contestid \"{contest_id}\" and sids {sids}...")
        running_progress = {}
        for sid in sids:
            running_progress[sid] = progress.add_task("[gray]Fetching results...[/gray]")
        session = get_session(console)
        while not progress.finished:
            res = session.get(f"https://atcoder.jp/contests/{contest_id}/submissions/status/json?{'&'.join([f'sids[]={sid}' for sid in sids])}")
            for sid in sids:
                status_string = res.json()['Result'].get(str(sid), {"Html":r'title="Not Found">.</span'})['Html']
                if "WJ" in status_string:
                    pass
                elif "waiting-judge" in status_string:
                    verdict, now, total = re.findall(r'title="(.+)">(\d+)/(\d+)\s*\S*</span', status_string)[0]
                    progress.update(running_progress[sid], description=f"[green]{sid}[/green]  {render_status(verdict)} | Running on {now}/{total}...", total = int(total), completed = int(now))
                else:
                    verdict = re.findall(r'title="(.+)">\S*</span', status_string)[0]
                    progress.update(running_progress[sid], description=f"[green]{sid}[/green]  {render_status(verdict)}", completed = 1, total = 1)
            sleep(1)

def handle(console:Console, args):
    console.log("[yellow]warn:you needn't call it most of the time, run \"atcli submit\" will automatically run this with sid.")
    fetch_result(console, args.contest_id, args.submissions)

if __name__ == '__main__':
    pass

