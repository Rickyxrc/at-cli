"""
This module is used to build mo file.
"""
# pylint: skip-file
# NOTE: I'm very sorry for this, but this script doesn't follow snake_case

import pathlib
import subprocess


def create_mo_files(_):
    print("Building mo files...")
    for lang in ["zh_CN"]:
        base_path = (
            pathlib.Path(__file__).parent.parent
            / "atcodercli"
            / "locales"
            / lang
            / "LC_MESSAGES"
        )
        res = subprocess.run(
            [
                "pybabel",
                "compile",
                "-i",
                str(base_path / "atcodercli.po"),
                "-o",
                str(base_path / "atcodercli.mo"),
            ],
            cwd=base_path,
            check=False,
        )
        if res.returncode:
            print(f"Failed when build {base_path / 'atcodercli.po'}")
            raise SystemExit(1)


if __name__ == "__main__":
    create_mo_files({})
