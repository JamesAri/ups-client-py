import sys
import threading
from game import start_game
from client import Client


def get_client() -> Client:
    if len(sys.argv) != 2:
        raise Exception("invalid arguments")
    else:
        return Client(sys.argv[1])


if __name__ == "__main__":
    client: Client = get_client()
    print(1)
    client.login()
    print(2)
    receive_thread = threading.Thread(target=client.receive)
    print(3)
    receive_thread.start()
    print(4)
    start_game(client)
    print(5)
    receive_thread.join()
    print(6)

# TODO: server - buffer - 1 per instance
# TODO: client - send deltas, not whole canvas
