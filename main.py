from settings import PORT
from game import start_game
from client import Client
from utils import get_valid_username, validate_username

import sys
import threading

EXPECTED_ARGUMENT = 2  # <script_path> | username


def get_client() -> Client:
    if len(sys.argv) != EXPECTED_ARGUMENT:
        raise Exception("invalid arguments")
    else:
        username = sys.argv[1]
        if not validate_username(username):
            username = get_valid_username()
        return Client(username, '127.0.0.1', PORT)


if __name__ == "__main__":
    client: Client = get_client()

    client.login()

    receive_thread = threading.Thread(target=client.receive)
    receive_thread.start()

    start_game(client)

    receive_thread.join()
