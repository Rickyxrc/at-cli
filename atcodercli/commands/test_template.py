import os
import pathlib
import subprocess

from rich.console import Console
from rich.progress import Progress

from atcodercli.utils.config import Config

from ..utils.problems import get_problem_name, load_parent_of_problem


# https://stackoverflow.com/a/21978778/19706510
def log_subprocess_output(pipe, prefix: str, console: Console):
    """
    Print output of a subprocess with a prefix.
    """
    for line in iter(pipe.readline, b""):
        console.print(prefix, str(line, encoding="utf-8"), end="")


def handle(console: Console, args):
    """
    Entry of cli, handle args.
    """
    problems = load_parent_of_problem(os.getcwd(), console)
    config = Config(console)
    contest_id, problem_id = get_problem_name(os.getcwd(), problems, console)
    found = False
    for index, problem in enumerate(problems.dat["problems"]):
        if problem["contest_id"] == contest_id and problem["problem_id"] == problem_id:
            found = True
            if args.file is None:
                if problem["templates"] == []:
                    console.print(
                        "[red]"
                        + _("problem %s_%s have no any code.")
                        % (contest_id, problem_id)
                        + "[/red]"
                    )
                    console.print(
                        _('please generate one using "atcli template generate"')
                    )
                    raise SystemExit(1)
                file = problem["templates"][0]
            else:
                file = args.file
            break

    if not found:
        console.print(
            "[red]"
            + _("problem %s_%s not found!") % (contest_id, problem_id)
            + "[/red]"
        )
        raise SystemExit(1)
    # console.print(f"testing file {file['path']} with template \"{file['template']}\"...")
    console.print(
        _('testing file %s with template "%s"...') % (file["path"], file["template"])
    )
    tests = config.dat["template"]["types"][file["template"]]["test"]
    run_env = os.environ.copy()
    run_env["FILE"] = file["path"]
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
    if args.checker is None:
        checker = config.dat["checker"]["default"]
    else:
        if config.dat["checker"].get(args.checker) is None:
            console.print(
                "[red]"
                + _('checker "%s" not found in config file.') % args.checker
                + "[/red]"
            )
            raise SystemExit(1)
        checker = args.checker
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
        else:
            console.print("[red]" + _("Some checks failed.") + "[/red]")
            for failed_check in failed:
                console.print(
                    "[red]"
                    + _('check %d failed, files are "%s" "%s"') % failed_check
                    + "[/red]"
                )
