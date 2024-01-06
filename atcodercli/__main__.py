import rich, argparse
from .login import handle as handleLogin
from .loginstat import handle as handleLoginStat

def dispatch_args():
    parser = argparse.ArgumentParser(
        prog = "atcli",
        description = "A lightweight, fast and beautiful command line interface for Atcoder.jp",
        epilog = '''
            default config path: ~/.config/atcli/config.yaml
            default login session path: ~/.config/atcli/session.yaml
            program source: https://github.com/rickyxrc/atcli
        ''',
    )

    OPERATIONS = {
        "login" : handleLogin,
        "loginstat" : handleLoginStat
    }
    parser.add_argument(
        "operation",
        type = str,
        choices = OPERATIONS.keys()
    )
    arg = parser.parse_args()

    console = rich.console.Console()

    OPERATIONS[arg.operation](console)

if __name__ == '__main__':
    dispatch_args()

