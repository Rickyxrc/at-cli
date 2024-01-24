import subprocess


def create_mo_files(setup_kwargs):
    print("Building mo files...")
    for lang in ["zh_CN"]:
        subprocess.run(
            [
                "pybabel",
                "compile",
                "-i",
                "./atcodercli/locales/%s/LC_MESSAGES/atcodercli.po" % lang,
                "-o",
                "./atcodercli/locales/%s/LC_MESSAGES/atcodercli.mo" % lang,
            ]
        )


if __name__ == "__main__":
    create_mo_files({})
