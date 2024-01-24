"""
This helper function is used to let user confirm a operation(with default value)
"""
from rich.console import Console


def confirm(
    console: Console,
    text: str,
    default: str = "type default selection here(yes or no), not required",
):
    """
    Let user confirm a operation(with default value)
    """
    inputyes = ["y", "yes"]
    inputno = ["n", "no"]

    hint_str = "\\[y/n]"
    if default.lower() in inputyes:
        hint_str = "\\[Y/n]"
    if default.lower() in inputno:
        hint_str = "\\[y/N]"

    while True:
        choice = console.input(f"{text} {hint_str}:")
        if choice == "":
            if default.lower() in inputyes:
                return True
            if default.lower() in inputno:
                return False
            console.print(r"this input have no default operation.")
        if choice.lower() in inputyes:
            return True
        if choice.lower() in inputno:
            return False
        console.print(r'Type "y"("yes") or "n"("no") please.')


if __name__ == "__main__":
    print(confirm(Console(), "(test) confirm this operation?", "yes"))
    print(confirm(Console(), "(test) confirm this operation?", "No"))
    print(confirm(Console(), "(test) confirm this operation?"))
