"""
    This module is used to watch a result of record(s) until judge ends
    You needn't to call it most of time
"""

import re
from time import sleep

import requests
from rich.console import Console
from rich.progress import Progress


def render_status(stat: str) -> str:
    """
    Render status string to rich-formatted string.
    Args:
        stat(str): status string from Atcoder.
    Returns:
        rendered string.
    Examples:
        render_status("Accepted") -> "[green]Accepted[/green]"
    """
    return {
        "Judging": "[gray]" + _("Judging") + "[/gray]",
        "Accepted": "[green]" + _("Accepted") + "[/green]",
        "Time Limit Exceeded": "[yellow]" + _("Time Limit Exceeded") + "[/yellow]",
        "Runtime Error": "[yellow]" + _("Runtime Error") + "[/yellow]",
        "Compilation Error": "[yellow]" + _("Compilation Error") + "[/yellow]",
        "Wrong Answer": "[yellow]" + _("Wrong Answer") + "[/yellow]",
        "Not Found": _("Not Found"),
    }.get(stat, _("Unknown status %s") % stat)


def watch_result(
    console: Console, contest_id: str, session: requests.Session, sids: list[int]
) -> list[bool]:
    """
    Render a list of records until judge ends.
    Args:
        contest_id(str): The id of a contest.
        sids(list[str]): The id(s) of a contest.
        console(Console): Console object from rich.console.
    Returns:
        list[bool] (accepted or not), outputs are rendered.
    """
    status = [False for _ in sids]
    with Progress(console=console) as progress:
        console.print(
            _('Getting result with contestid "%s" and sids %s...') % (contest_id, sids)
        )
        running_progress = {}
        for sid in sids:
            running_progress[sid] = progress.add_task(
                "[gray]" + _("Getting results...") + "[/gray]"
            )
        while not progress.finished:
            res = session.get(
                f"https://atcoder.jp/contests/{contest_id}"
                f"/submissions/status/json?{'&'.join([f'sids[]={sid}' for sid in sids])}"
            )
            for index, sid in enumerate(sids):
                status_string = res.json()["Result"].get(
                    str(sid), {"Html": r'title="Not Found">.</span'}
                )["Html"]
                # console.print(sids, res.json())
                if "WJ" in status_string:
                    pass
                elif "waiting-judge" in status_string:
                    verdict, now, total = re.findall(
                        r'title="(.+)">(\d+)/(\d+)\s*\S*</span', status_string
                    )[0]
                    progress.update(
                        running_progress[sid],
                        description=f"[green]{sid}[/green] {render_status(verdict)}"
                        " | " + _("Running on %d/%d...") % (int(now), int(total)),
                        total=int(total),
                        completed=int(now),
                    )
                else:
                    verdict = re.findall(r'title="(.+)">\S*</span', status_string)[0]
                    progress.update(
                        running_progress[sid],
                        description=f"[green]{sid}[/green] {render_status(verdict)}",
                        completed=1,
                        total=1,
                    )
                    status[index] = verdict == "Accepted"
            sleep(1)
        return status


def handle(console: Console, session: requests.Session, args):
    """
    Entry of cli, handle args.
    """
    console.print(
        "[yellow]"
        + _(
            "warn:you needn't call it most of the time, "
            'run "atcli submit" will automatically run this with sid.'
        )
    )
    watch_result(console, args.contest_id, session, args.submissions)


if __name__ == "__main__":
    pass
