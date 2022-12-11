from game import start_game
from client import Client
from utils import get_valid_username, validate_username

import sys
import threading

EXPECTED_ARGUMENTS = 4  # <script_path> | username hostname port


def get_client() -> Client:
    if len(sys.argv) != EXPECTED_ARGUMENTS:
        print("usage: <executable> username hostname port", file=sys.stderr)
        exit(1)

    username = sys.argv[1]
    host = sys.argv[2]
    port = 0
    try:
        port = int(sys.argv[3])
    except ValueError:
        print("Invalid port number", file=sys.stderr)
        exit(1)

    if not validate_username(username):
        username = get_valid_username()
        
    return Client(username, host, port)


if __name__ == "__main__":
    client: Client = get_client()

    client.login()

    receive_thread = threading.Thread(target=client.receive)
    receive_thread.start()

    start_game(client)

    receive_thread.join()
