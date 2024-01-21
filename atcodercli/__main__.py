"""
Main Module of atcli
"""
import argparse

import rich

from .commands.addproblem import handle as handleAddProblem
from .commands.initcontest import handle as handleInitContest
from .commands.initproblem import handle as handleInitProblem
from .commands.inittemplate import handle as handleInitTemplate
from .commands.login import handle as handleLogin
from .commands.me import handle as handleMe
from .commands.watchpage import handle as handleWatchPage
from .commands.watchresult import handle as handleWatchResult
from .commands.testtemplate import handle as handleTestTemplate

def dispatch_args():
    """
    dispatch argument(from command line)
    the main entry of cli
    """
    console = rich.console.Console()
    try:
        parser = argparse.ArgumentParser(
            prog = "atcli",
            description = "A lightweight, fast and beautiful command line interface for Atcoder.jp",
            epilog = '''
                default config path: ~/.config/atcli/config.yaml
                default login session path: ~/.config/atcli/session.yaml
                program source: https://github.com/rickyxrc/atcli
            ''',
        )

        subparsers = parser.add_subparsers(dest="command", required=True)
        login_parser = subparsers.add_parser(
            "login",
            help = "login with your username and password,"
                " the session will stored in ~/.config/atcli/session.yaml"
        )
        me_parser = subparsers.add_parser(
            "me",
            help="check if your session file is valid"
        )

        result_parser = subparsers.add_parser(
            "result",
            help="watch submission's results"
        )
        result_subparsers = result_parser.add_subparsers(
            dest="result_subcommand",
            required=True
        )
        result_watch_parser = result_subparsers.add_parser(
            "watch",
            help="watch a specific submission id's result"
        )
        result_watch_parser.add_argument(
            "contest_id",
            help="The id of the contest, like 'abc123'"
        )
        result_watch_parser.add_argument(
            "submissions",
            help="The submission id of the contest",
            nargs='+'
        )
        result_page_parser = result_subparsers.add_parser(
            "page",
            help="watch a contest's latest submissions"
        )
        result_page_parser.add_argument(
            "contest_id",
            help="The id of the contest, like 'abc123'"
        )

        problem_parser = subparsers.add_parser(
            "problem",
            help="operate with problems(like submit, add)"
        )
        problem_subparsers = problem_parser.add_subparsers(
            dest = "problem_subcommand",
            required = True
        )
        problem_add_parser = problem_subparsers.add_parser(
            "add",
            help = "add a problem to solve"
        )
        problem_add_parser.add_argument(
            "contest_id",
            help = "The id of the contest, like 'abc123'"
        )
        problem_add_parser.add_argument(
            "problem_id",
            help = "The id of the problem, like 'a' or 'g'"
        )
        problem_init_parser = problem_subparsers.add_parser(
            "init",
            help = "init problem.yaml in current dir"
        )
        problem_init_parser.add_argument(
            "--force",
            action = "store_true"
        )
        contest_parser = subparsers.add_parser(
            "contest",
            help = "operate with contests(pull all problem samples)"
        )
        contest_subparsers = contest_parser.add_subparsers(
            dest = "contest_subcommand",
            required = True
        )
        contest_race_parser = contest_subparsers.add_parser(
            "race",
            help = "init a problem.yaml locally and pull all problem samples"
        )
        contest_race_parser.add_argument(
            "contest_id",
            help = "The id of the contest, like 'abc123'"
        )
        contest_race_parser.add_argument(
            "--force",
            action = "store_true"
        )
        contest_race_parser.add_argument(
            "--template",
            help = "specific template type"
        )
        template_parser = subparsers.add_parser(
            "template",
            help = "init with template, run template commands(like test)"
        )
        template_subparsers = template_parser.add_subparsers(
            dest = "template_subcommand",
            required = True
        )
        template_init_parser = template_subparsers.add_parser(
            "init",
            help = "init a template under current dir(need \"atcli contest racce\" or \"atcli problem init\"), template name is dirname default, a \"problem.yaml\" should exist exactly pwd's parent dir."
        )
        template_init_parser.add_argument(
            "--name",
            help = "specific generated file name"
        )
        template_init_parser.add_argument(
            "--template",
            help = "specific template type(or using the default)"
        )
        template_init_parser.add_argument(
            "--force",
            action = "store_true"
        )
        template_test_parser = template_subparsers.add_parser(
            "test",
            help = "test a templete defined in config."
        )
        template_test_parser.add_argument(
            "--file",
            help = "specific file to test(or test the default)"
        )
        template_test_parser.add_argument(
            "--checker",
            help = "specific checker to use"
        )

        arg = parser.parse_args()
        if arg.command == 'login':
            handleLogin(console, arg)
        if arg.command == 'me':
            handleMe(console, arg)
        if arg.command == 'result':
            if arg.result_subcommand == 'watch':
                handleWatchResult(console, arg)
            if arg.result_subcommand == 'page':
                handleWatchPage(console, arg)
        if arg.command == 'problem':
            if arg.problem_subcommand == 'add':
                handleAddProblem(console, arg)
            if arg.problem_subcommand == 'init':
                handleInitProblem(console, arg)
        if arg.command == 'contest':
            if arg.contest_subcommand == 'race':
                handleInitContest(console, arg)
        if arg.command == 'template':
            if arg.template_subcommand == 'init':
                handleInitTemplate(console, arg)
            if arg.template_subcommand == 'test':
                handleTestTemplate(console, arg)

    except KeyboardInterrupt:
        console.print("[red]FATAL:Interrupted.[/red]")

if __name__ == '__main__':
    dispatch_args()
