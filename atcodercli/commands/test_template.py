"""
    Test a template use config defined in ~/.config/atcli/config.yaml
"""
import os
import pathlib
import subprocess

from rich.console import Console
from rich.progress import Progress
from rich.text import Text

from atcodercli.utils.config import Config

from ..utils.problems import get_problem_name, load_parent_of_problem


# Eval ansi code: https://stackoverflow.com/a/73284729/19706510
# Read Line from subprocess: https://stackoverflow.com/a/21978778/19706510
def log_subprocess_output(pipe, prefix: str, console: Console):
    """
    Print output of a subprocess with a prefix.
    """
    for line in iter(pipe.readline, b""):
        ansi_text = Text.from_ansi(str(line, encoding="utf-8"))
        console.print(prefix, ansi_text)


def test_template(
    path: pathlib.Path,
    template: str,
    checker: str,
    config: Config,
    console: Console,
) -> bool:
    """
    Test a template and return succeed or not.
    """
    # contest_id, problem_id = get_problem_name(path.parent, problems, console)

    console.print(
        _('testing file %s with template "%s" and checker "%s"...')
        % (path, template, checker)
    )
    tests = config.dat["template"]["types"][template]["test"]
    run_env = os.environ.copy()
    run_env["FILE"] = path
    path = pathlib.Path(os.getcwd())
    test_files = []
    tot_files = os.listdir(path)
    for file in tot_files:
        file_without_ext = ".".join(file.split(".")[:-1])
        if (
            "." in file
            and file.split(".")[-1] == "in"
            and file_without_ext + ".ans" in tot_files
        ):
            test_files.append((file, f"{file_without_ext}.ans"))
    test_files = sorted(test_files)
    task_count = len(test_files)

    with Progress(console=console) as progress:
        test_task = progress.add_task(_("Waiting Judge..."), total=task_count)

        console.print(f"$ {tests['before']}")
        with subprocess.Popen(
            tests["before"],
            cwd=os.getcwd(),
            env=run_env,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
        ) as command_init:
            with command_init.stdout:
                log_subprocess_output(
                    command_init.stdout, "[blue]" + _("stdout:") + "[/blue]", console
                )
            with command_init.stderr:
                log_subprocess_output(
                    command_init.stderr, "[red]" + _("stderr:") + "[/red]", console
                )
            command_init_res = command_init.wait()
            if command_init_res != 0:
                console.print(
                    "[red]" + _("Pre-execute script return non-zero value") + "[/red]"
                )
                raise SystemExit(1)

        passed = 0
        failed = []
        for index, test in enumerate(test_files):
            progress.update(
                test_task, description=_("Running on %d/%d") % (index + 1, task_count)
            )
            run_env["INPUT"], run_env["ANSWER"] = test
            run_env["OUTPUT"] = "file.out"
            console.print(f"$ {tests['run']}")
            with subprocess.Popen(
                tests["run"],
                cwd=os.getcwd(),
                env=run_env,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
            ) as command_test:
                with command_test.stdout:
                    log_subprocess_output(
                        command_test.stdout,
                        "[blue]" + _("runner stdout:") + "[/blue]",
                        console,
                    )
                with command_test.stderr:
                    log_subprocess_output(
                        command_test.stderr,
                        "[red]" + _("runner stderr:") + "[/red]",
                        console,
                    )

            progress.update(test_task, advance=1)
            console.print(f"$ {config.dat['checker']['types'][checker]}")
            with subprocess.Popen(
                config.dat["checker"]["types"][checker],
                cwd=os.getcwd(),
                env=run_env,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
            ) as command_check:
                with command_check.stdout:
                    log_subprocess_output(
                        command_check.stdout,
                        "[blue]" + _("checker stdout:") + "[/blue]",
                        console,
                    )
                with command_check.stderr:
                    log_subprocess_output(
                        command_check.stderr,
                        "[red]" + _("checker stderr:") + "[/red]",
                        console,
                    )
                res = command_check.wait()
            if res:
                console.print(
                    "[red]"
                    + _("Test %d Failed - checker returned non-zero value")
                    % (index + 1)
                    + "[/red]"
                )
                failed.append((index + 1, test[0], test[1]))
            else:
                console.print(
                    "[green]" + _("Test %d Passed") % (index + 1) + "[/green]"
                )
                passed += 1

        console.print("---------------" + _("TEST SUMMARY") + "---------------")
        if passed == task_count:
            console.print("[green]" + _("All check passed!") + "[/green]")
            return True
        else:
            console.print("[red]" + _("Some checks failed.") + "[/red]")
            for failed_check in failed:
                console.print(
                    "[red]"
                    + _('check %d failed, files are "%s" "%s"') % failed_check
                    + "[/red]"
                )
            return False


def handle(console: Console, args) -> bool:
    """
    Entry of cli, handle args.
    """
    # TODO: change path when args.template set
    path = pathlib.Path(os.getcwd())
    problems = load_parent_of_problem(os.getcwd(), console)
    contest_id, problem_id = get_problem_name(path, problems, console)
    current_problem = problems.get_by_contest_problem_id(contest_id, problem_id)
    config = Config(console)
    if current_problem["accepted"] is True:
        console.print(
            "[yellow]" + _("This problem is marked as accepted.") + "[/yellow]"
        )
    if args.file is None:
        file = problems.get_default_file(contest_id, problem_id)
    else:
        try:
            file = problems.get_by_contest_problem_id_file(
                contest_id, problem_id, args.file
            )
        except FileNotFoundError as exception:
            console.print("[red]" + _("file %s not found") % args.file + "[/red]")
            raise SystemExit(1) from exception
    if args.checker is None:
        checker = config.dat["checker"]["default"]
    else:
        if config.dat["checker"]["types"].get(args.checker) is None:
            console.print(
                "[red]"
                + _('checker "%s" not exist in config.') % args.checker
                + "[/red]"
            )
            raise SystemExit(1)
        checker = args.checker
    if args.template is None:
        template = file["template"]
    else:
        if config.dat["template"]["types"].get(args.template) is None:
            console.print(
                "[red]"
                + _('template "%s" not exist in config') % args.template
                + "[/red]"
            )
            raise SystemExit(1)
        template = args.template
    return test_template(
        pathlib.Path(file["path"]),
        template,
        checker,
        config,
        console,
    )
