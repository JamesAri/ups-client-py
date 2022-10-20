import sys
import threading
import time

from game import start_game
from client import Client
from settings import MAX_USERNAME_LEN


def get_client() -> Client:
    if len(sys.argv) != 2:
        raise Exception("invalid arguments")
    else:
        if len(sys.argv[1]) > MAX_USERNAME_LEN:
            raise Exception(f"Username can have max. {MAX_USERNAME_LEN} characters")
        return Client(sys.argv[1])


if __name__ == "__main__":
    client: Client = get_client()

    client.login()

    receive_thread = threading.Thread(target=client.receive)
    receive_thread.start()

    start_game(client)

    receive_thread.join()
