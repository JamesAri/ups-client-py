import sys
import threading
from game import start_game
from client import Client


def get_client() -> Client:
    if len(sys.argv) != 2:
        exit(1)
    else:
        return Client(sys.argv[1])


if __name__ == "__main__":
    client: Client = get_client()

    client.login()

    receive_thread = threading.Thread(target=client.receive)
    receive_thread.start()

    # send_thread = threading.Thread(target=client.send)
    # send_thread.start()

    start_game(client)

    receive_thread.join()
    # send_thread.join()
