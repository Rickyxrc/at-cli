import rich, argparse
from commands.login import handle as handleLogin
from commands.me import handle as handleMe
from commands.watchpage import handle as handleWatchPage
from commands.watchresult import handle as handleWatchResult

def dispatch_args():
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

        subparsers = parser.add_subparsers(dest="command", help="sub command", required=True)
        login_parser = subparsers.add_parser("login", help = "login with your username and password, the session will stored in ~/.config/atcli/session.yaml")
        me_parser = subparsers.add_parser("me", help="check if your session file is valid")

        result_parser = subparsers.add_parser("result", help="watch submission's results")
        result_subparsers = result_parser.add_subparsers(dest="result_subcommand", help = "result's subcommand", required=True)
        result_watch_parser = result_subparsers.add_parser("watch", help="watch a specific submission id's result")
        result_watch_parser.add_argument("contest_id", help="The id of the contest, like 'abc123'")
        result_watch_parser.add_argument("submissions", help="The submission id of the contest", nargs='+')
        result_page_parser = result_subparsers.add_parser("page", help="watch a contest's latest submissions")
        result_page_parser.add_argument("contest_id", help="The id of the contest, like 'abc123'")

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

    except KeyboardInterrupt:
        console.log("[red]FATAL:Interrupted.[/red]")

if __name__ == '__main__':
    dispatch_args()

