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
        console.log(prefix, str(line, encoding="utf-8"))

def handle(console:Console, args):
    problems = tryLoadProblemInProblem(os.getcwd(), console)
    config = Config(console)
    contest_id, problem_id = getProblemName(os.getcwd(), problems, console)
    found = False
    for index, problem in enumerate(problems.dat['problems']):
        if problem['contest_id'] == contest_id and problem['problem_id'] == problem_id:
            # console.log(index, problem)
            found = True
            if args.file == None:
                if problem['templates'] == []:
                    console.log(f"[red]problem {contest_id}_{problem_id} have no any code.[/red]")
                    console.log("please generate one using \"atcli template generate\"")
                    raise SystemExit(1)
                file = problem['templates'][0]
            else:
                file = args.file
            break
    if not found:
        console.log(f"[red]problem {contest_id}_{problem_id} not found![/red]")
        raise SystemExit(1)
    console.log(f"testing file {file['path']} with template \"{file['template']}\"...")
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
            console.log(f"[red]checker \"{args.checker}\" not found in config file.[/red]")
            raise SystemExit(1)
        checker = args.checker
    with Progress(console=console) as progress:
        test_task = progress.add_task("Waiting Judge...", total = totalTask)

        console.log(f"$ {tests['before']}")
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
            log_subprocess_output(command_init.stdout, "[blue]stdout:[/blue]", console)
        with command_init.stderr:
            log_subprocess_output(command_init.stderr, "[red]stderr:[/red]", console)

        passed = 0
        failed = []
        for index, test in enumerate(test_files):
            progress.update(test_task, description=f"Running {index+1}/{totalTask}")
            run_env['INPUT'], run_env['ANSWER'] = test
            run_env['OUTPUT'] = "file.out"
            console.log(f"$ {tests['run']}")
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
                log_subprocess_output(command_test.stdout, "[blue]runner stdout:[/blue]", console)
            with command_test.stderr:
                log_subprocess_output(command_test.stderr, "[red]runner stderr:[/red]", console)

            progress.update(test_task, advance=1)
            console.log(f"$ {config.dat['checker']['types'][checker]}")
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
                log_subprocess_output(command_check.stdout, "[blue]checker stdout:[/blue]", console)
            with command_check.stderr:
                log_subprocess_output(command_check.stderr, "[red]checker stderr:[/red]", console)
            res = command_check.wait()
            if res:
                console.log(f"[red]Test {index+1} Failed - checker returned non-zero value[/red]")
                failed.append((index+1, test[0], test[1]))
            else:
                console.log(f"[green]Test {index+1} Passed[/green]")
                passed += 1
        console.log("---------------SUMMARY---------------")
        if passed == totalTask:
            console.log("[green]All check passed![/green]")
        else:
            console.log("[red]Some checks failed.[/red]")
            for failedCheck in failed:
                # console.log(failedCheck)
                console.log(f"[red]check {failedCheck[0]} failed, files are \"{failedCheck[1]}\" \"{failedCheck[2]}\"")
