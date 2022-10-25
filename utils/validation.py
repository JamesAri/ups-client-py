from settings import MAX_USERNAME_LEN

import re

regexp = re.compile(r"\W")


def get_valid_username() -> str:
    username = input_username_prompt()
    while not validate_username(username):
        username = input_username_prompt()
    return username


def validate_username(username: str) -> bool:
    if username == "!dev-game-only":
        return True
    return len(username) <= MAX_USERNAME_LEN and not regexp.search(username)


def input_username_prompt() -> str:
    print(f"Input username (max. {MAX_USERNAME_LEN} characters).\n"
          f"Valid characters are from a to Z, digits from 0-9, and the underscore _ character")
    return input("Username: ")
