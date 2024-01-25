"""
This module is used to submit a problem and watch its result
"""
import os
import pathlib

from rich.console import Console

from ..utils.config import Config
from ..utils.get_session import get_csrf, get_session
from ..utils.problems import get_problem_name, load_parent_of_problem
from .test_template import handle as handleTestTemplate
from .watch_page import get_list
from .watch_result import watch_result


def handle(console: Console, args):
    """
    Entry of cli, handle args.
    """
    if not (args.no_check or args.force):
        test_result = handleTestTemplate(console, args)
        if test_result is False:
            console.print(
                "[red]" + _("interruped because pretest not passed") + "[/red]"
            )
            console.print(_("to ignore local check, use --no-check or --force"))
            return
    path = pathlib.Path(os.getcwd())
    problems = load_parent_of_problem(path, console)
    config = Config(console)
    contest_id, problem_id = get_problem_name(path, problems, console)
    if problems.get_by_contest_problem_id(contest_id, problem_id)["accepted"] and not (
        args.ignore_accepted or args.force
    ):
        console.print("[red]" + _("This problem is marked as accepted.") + "[/red]")
        console.print(_("to override, use --ignore-accepted or --force"))
        raise SystemExit(1)
    if args.file is None:
        test_file = problems.get_default_file(contest_id, problem_id)["path"]
    else:
        test_file = args.file
    file = problems.get_by_contest_problem_id_file(contest_id, problem_id, test_file)
    template = args.template if args.template is not None else file["template"]
    session = get_session(console)
    with open(file["path"], "r", encoding="utf-8") as file:
        post_data = {
            "data.TaskScreenName": f"{contest_id}_{problem_id}",
            "data.LanguageId": config.dat["template"]["types"][template]["lang_id"],
            "sourceCode": file.read(),
            "csrf_token": get_csrf(
                session, console, f"https://atcoder.jp/contests/{contest_id}/submit"
            ),
        }
        # submit problem
        console.print(_("Submitting problem %s") % (f"{contest_id}_{problem_id}"))
        session.post(f"https://atcoder.jp/contests/{contest_id}/submit", data=post_data)
        lis = get_list(
            f"https://atcoder.jp/contests/{contest_id}/submissions/me", session
        )
        watch_result(console, contest_id, lis)
