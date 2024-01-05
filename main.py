import rich, argparse, importlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "at-cli",
        description = "A lightweight, fast and beautiful command line interface for Atcoder.jp",
        epilog = '''
            default config path: ~/.config/at-cli/config.yaml
            default login session path: ~/.config/at-cli/session.yaml
            program source: https://github.com/rickyxrc/at-cli
        ''',
    )

    OPERATIONS = {
        "login" : importlib.import_module("src.login").handle
    }
    parser.add_argument(
        "operation",
        type = str,
        choices = OPERATIONS.keys()
    )
    arg = parser.parse_args()

    console = rich.console.Console()

    OPERATIONS[arg.operation](console)

