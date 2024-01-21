import os
import subprocess
import pathlib

from atcodercli.utils.config import Config
from ..utils.problems import getProblemName, tryLoadProblemInProblem

from rich.console import Console
from rich.progress import Progress

# https://stackoverflow.com/a/21978778/19706510
def log_subprocess_output(pipe, prefix:str, console:Console):
    for line in iter(pipe.readline, b''):
        console.print(prefix, str(line, encoding="utf-8"), end="")

def handle(console:Console, args):
    problems = tryLoadProblemInProblem(os.getcwd(), console)
    config = Config(console)
    contest_id, problem_id = getProblemName(os.getcwd(), problems, console)
    found = False
    for index, problem in enumerate(problems.dat['problems']):
        if problem['contest_id'] == contest_id and problem['problem_id'] == problem_id:
            # console.print(index, problem)
            found = True
            if args.file == None:
                if problem['templates'] == []:
                    console.print("[red]" + _("problem %s_%s have no any code.") % (contest_id, problem_id) + "[/red]")
                    console.print(_("please generate one using \"atcli template generate\""))
                    raise SystemExit(1)
                file = problem['templates'][0]
            else:
                file = args.file
            break
    if not found:
        console.print("[red]" + _("problem %s_%s not found!") % (contest_id, problem_id) + "[/red]")
        raise SystemExit(1)
    # console.print(f"testing file {file['path']} with template \"{file['template']}\"...")
    console.print(_("testing file %s with template \"%s\"...") % (file['path'], file['template']))
    tests = config.dat['template']['types'][file['template']]['test']
    run_env = os.environ.copy()
    run_env['FILE'] = file['path']
    path = pathlib.Path(os.getcwd())
    test_files = []
    tot_files = os.listdir(path)
    for file in tot_files:
        fileWithoutExt = '.'.join(file.split('.')[:-1])
        if '.' in file and file.split('.')[-1] == 'in' and fileWithoutExt+'.ans' in tot_files:
            test_files.append((file, f"{fileWithoutExt}.ans"))
    test_files = sorted(test_files)
    totalTask = len(test_files)
    if args.checker == None:
        checker = config.dat['checker']['default']
    else:
        if config.dat['checker'].get(args.checker) == None:
            console.print("[red]" + _("checker \"%s\" not found in config file.") % args.checker + "[/red]")
            raise SystemExit(1)
        checker = args.checker
    with Progress(console=console) as progress:
        test_task = progress.add_task(_("Waiting Judge..."), total = totalTask)

        console.print(f"$ {tests['before']}")
        command_init = subprocess.Popen(
            tests['before'],
            cwd=os.getcwd(),
            env=run_env,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL
        )
        with command_init.stdout:
            log_subprocess_output(command_init.stdout, "[blue]" + _("stdout:") + "[/blue]", console)
        with command_init.stderr:
            log_subprocess_output(command_init.stderr, "[red]" + _("stderr:") + "[/red]", console)

        passed = 0
        failed = []
        for index, test in enumerate(test_files):
            progress.update(test_task, description = _("Running on %d/%d") % (index+1, totalTask))
            run_env['INPUT'], run_env['ANSWER'] = test
            run_env['OUTPUT'] = "file.out"
            console.print(f"$ {tests['run']}")
            command_test = subprocess.Popen(
                tests['run'],
                cwd=os.getcwd(),
                env=run_env,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL
            )
            with command_test.stdout:
                log_subprocess_output(command_test.stdout, "[blue]" + _("runner stdout:") + "[/blue]", console)
            with command_test.stderr:
                log_subprocess_output(command_test.stderr, "[red]" + _("runner stderr:") + "[/red]", console)

            progress.update(test_task, advance=1)
            console.print(f"$ {config.dat['checker']['types'][checker]}")
            command_check = subprocess.Popen(
                config.dat['checker']['types'][checker],
                cwd=os.getcwd(),
                env=run_env,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL
            )
            with command_check.stdout:
                log_subprocess_output(command_check.stdout, "[blue]" + _("checker stdout:") + "[/blue]", console)
            with command_check.stderr:
                log_subprocess_output(command_check.stderr, "[red]" + _("checker stderr:") + "[/red]", console)
            res = command_check.wait()
            if res:
                console.print("[red]" + _("Test %d Failed - checker returned non-zero value") % (index+1) + "[/red]")
                failed.append((index+1, test[0], test[1]))
            else:
                console.print("[green]" + _("Test %d Passed") % (index+1) + "[/green]")
                passed += 1
        console.print("---------------" + _("TEST SUMMARY") + "---------------")
        if passed == totalTask:
            console.print("[green]" + _("All check passed!") + "[/green]")
        else:
            console.print("[red]" + _("Some checks failed.") + "[/red]")
            for failedCheck in failed:
                console.print("[red]" + _("check %d failed, files are \"%s\" \"%s\"") % failedCheck + "[/red]")

