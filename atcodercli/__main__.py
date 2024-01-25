"""
Main Module of atcli
"""
# TODO: input the config and problem object here to reuse
import argparse

import rich

from .commands.add_problem import handle as handleAddProblem
from .commands.init_contest import handle as handleInitContest
from .commands.init_problem import handle as handleInitProblem
from .commands.init_template import handle as handleInitTemplate
from .commands.login import handle as handleLogin
from .commands.me import handle as handleMe
from .commands.submit_problem import handle as handleSubmitProblem
from .commands.test_template import handle as handleTestTemplate
from .commands.watch_page import handle as handleWatchPage
from .commands.watch_result import handle as handleWatchResult


def dispatch_args():
    """
    dispatch argument(from command line)
    the main entry of cli
    """
    console = rich.console.Console()
    try:
        parser = argparse.ArgumentParser(
            prog="atcli",
            description=_(
                "at-cli, a lightweight, cross-platform, fast and beautiful command line interface for https://atcoder.jp"
            ),
            epilog=_(
                "default config path: ~/.config/atcli/config.yaml\n"
                "default login session path: ~/.config/atcli/session.yaml\n"
                "program source: https://github.com/rickyxrc/atcli\n"
            ),
        )

        subparsers = parser.add_subparsers(dest="command", required=True)

        # pylint: disable=unused-variable
        login_parser = subparsers.add_parser(
            "login",
            help=_(
                "login with your username and password,"
                " the session will stored in ~/.config/atcli/session.yaml"
            ),
        )

        # pylint: disable=unused-variable
        me_parser = subparsers.add_parser(
            "me", help=_("check if your session file is valid")
        )

        result_parser = subparsers.add_parser(
            "result", help=_("watch submission's results")
        )
        result_subparsers = result_parser.add_subparsers(
            dest="result_subcommand", required=True
        )
        result_watch_parser = result_subparsers.add_parser(
            "watch", help=_("watch a specific submission id's result")
        )
        result_watch_parser.add_argument(
            "contest_id", help=_("The id of the contest, like 'abc123'")
        )
        result_watch_parser.add_argument(
            "submissions", help=_("The submission id of the contest"), nargs="+"
        )
        result_page_parser = result_subparsers.add_parser(
            "page", help=_("watch a contest's latest submissions")
        )
        result_page_parser.add_argument(
            "contest_id", help=_("The id of the contest, like 'abc123'")
        )

        problem_parser = subparsers.add_parser(
            "problem", help=_("operate with problems(like submit, add)")
        )
        problem_subparsers = problem_parser.add_subparsers(
            dest="problem_subcommand", required=True
        )
        problem_add_parser = problem_subparsers.add_parser(
            "add", help=_("add a problem to solve")
        )
        problem_add_parser.add_argument(
            "contest_id", help=_("The id of the contest, like 'abc123'")
        )
        problem_add_parser.add_argument(
            "problem_id", help=_("The id of the problem, like 'a' or 'g'")
        )
        problem_add_parser.add_argument("--force", action="store_true")
        problem_add_parser.add_argument("--template", help=_("specific template type"))
        problem_add_parser.add_argument(
            "--name", help=_("specific generated file name")
        )
        problem_init_parser = problem_subparsers.add_parser(
            "init", help=_("init problem.yaml in current dir")
        )
        problem_init_parser.add_argument("--force", action="store_true")
        problem_submit_parser = problem_subparsers.add_parser(
            "submit", help=_("submit current problem")
        )
        problem_submit_parser.add_argument(
            "--no-check", help=_("ignore pretest check"), action="store_true"
        )
        problem_submit_parser.add_argument(
            "--ignore-accepted",
            help=_("submit this problem, though it's accepted"),
            action="store_true",
        )
        problem_submit_parser.add_argument(
            "--force", help=_("ignore all check, just submit the problem")
        )
        problem_submit_parser.add_argument(
            "--template", help=_("specific template type")
        )
        problem_submit_parser.add_argument(
            "--file", help=_("specific the file to submit")
        )
        problem_submit_parser.add_argument(
            "--checker", help=_("specific checker to use")
        )
        contest_parser = subparsers.add_parser(
            "contest", help=_("operate with contests(pull all problem samples)")
        )
        contest_subparsers = contest_parser.add_subparsers(
            dest="contest_subcommand", required=True
        )
        contest_init_parser = contest_subparsers.add_parser(
            "init",
            help=_("init a problem.yaml locally and pull all problem samples"),
            aliases=["race"],
        )
        contest_init_parser.add_argument(
            "contest_id", help=_("The id of the contest, like 'abc123'")
        )
        contest_init_parser.add_argument("--force", action="store_true")
        contest_init_parser.add_argument("--template", help=_("specific template type"))
        template_parser = subparsers.add_parser(
            "template", help=_("init with template, run template commands(like test)")
        )
        template_subparsers = template_parser.add_subparsers(
            dest="template_subcommand", required=True
        )
        template_init_parser = template_subparsers.add_parser(
            "init",
            aliases=["gen", "add"],
            help=_(
                'init a template under current dir(need "atcli contest racce" or "atcli problem init"), template name is dirname default, a "problem.yaml" should exist exactly pwd\'s parent dir.'
            ),
        )
        template_init_parser.add_argument(
            "--name", help=_("specific generated file name")
        )
        template_init_parser.add_argument(
            "--template", help=_("specific template type(or using the default)")
        )
        template_init_parser.add_argument("--force", action="store_true")
        template_test_parser = template_subparsers.add_parser(
            "test", help=_("test a templete defined in config.")
        )
        template_test_parser.add_argument("--file", help=_("specific file to test"))
        template_test_parser.add_argument(
            "--checker", help=_("specific checker to use")
        )
        template_test_parser.add_argument(
            "--template", help=_("override the template setting")
        )

        arg = parser.parse_args()
        if arg.command == "login":
            handleLogin(console, arg)
        if arg.command == "me":
            handleMe(console, arg)
        if arg.command == "result":
            if arg.result_subcommand == "watch":
                handleWatchResult(console, arg)
            if arg.result_subcommand == "page":
                handleWatchPage(console, arg)
        if arg.command == "problem":
            if arg.problem_subcommand == "add":
                handleAddProblem(console, arg)
            if arg.problem_subcommand == "init":
                handleInitProblem(console, arg)
            if arg.problem_subcommand == "submit":
                handleSubmitProblem(console, arg)
        if arg.command == "contest":
            if arg.contest_subcommand in ["init", "race"]:
                handleInitContest(console, arg)
        if arg.command == "template":
            if arg.template_subcommand in ["init", "gen", "add"]:
                handleInitTemplate(console, arg)
            if arg.template_subcommand == "test":
                handleTestTemplate(console, arg)

    except KeyboardInterrupt:
        console.print("[red]" + _("FATAL:Interrupted.") + "[/red]")


if __name__ == "__main__":
    dispatch_args()
