"""
This module is used to test the translation.
"""
import os
import pathlib
import subprocess
import sys


def readall(pipe) -> str:
    """
    Read all content from pipe
    """
    res = ""
    for line in iter(pipe.readline, b""):
        res += str(line, encoding="utf-8")
    return res


def run_command_and_get_output(lang: str, extra_args: list[str]) -> str:
    """
    Run a command and get output
    """
    assert extra_args != []
    assert lang != ""

    run_env = os.environ
    run_env["LANG"] = lang
    res = ""
    with subprocess.Popen(
        " ".join(["poetry", "run", "python", "-m", "atcodercli"] + extra_args),
        env=run_env,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        cwd=pathlib.Path(__file__).parent.parent,
    ) as command_test:
        with command_test.stdout:
            res += readall(command_test.stdout)
        with command_test.stderr:
            res += readall(command_test.stderr)
        returncode = command_test.wait()
        assert res != ""  # assert command is executed
        print(res)
        assert returncode == 0
    return res


def test_system_output():
    """
    Test output encoding, must be utf-8
    """
    assert sys.stdout.encoding == "utf-8"


def test_chinese_translation():
    """
    Test Chinese translation
    """
    res_str = run_command_and_get_output("zh_CN.UTF-8", ["--help"])
    assert "工具" in res_str


def test_english_translation():
    """
    Test English translation
    """
    res_str = run_command_and_get_output("en_US.UTF-8", ["--help"])
    assert "command" in res_str


def test_fallback_translation():
    """
    Test if this language is not supported
    """
    # This language is definitely not exist
    res_str = run_command_and_get_output("ricky_CN.UTF-8", ["--help"])
    assert "command" in res_str
    res_str = run_command_and_get_output("Definitelyinvalidlanguage", ["--help"])
    assert "command" in res_str
