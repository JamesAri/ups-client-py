import socket
import threading
import time as tm
from model import Chat, Canvas

from settings import CANVAS_SIZE_SERIALIZED, TIMEOUT_SEC


class Client:
    username: str
    server: socket
    run: threading.Event
    is_drawing: threading.Event
    game_in_progress: threading.Event
    correct_guess: threading.Event
    can_guess: threading.Event
    chat: Chat
    canvas: Canvas

    def __init__(self, username: str):
        self.username = username

        self.chat = Chat()
        self.canvas = Canvas()

        self.is_drawing = threading.Event()
        self.game_in_progress = threading.Event()
        self.correct_guess = threading.Event()
        self.can_guess = threading.Event()
        self.run = threading.Event()

        self.run.set()

    def login(self):
        if self.username == "!dev-game-only":
            return
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(('147.228.133.43', 53165))
            self.server.settimeout(TIMEOUT_SEC)

            my_bytes = bytearray([6])
            my_bytes += len(self.username).to_bytes(4, "big")
            my_bytes += bytearray(self.username, "ascii")
            self.server.send(my_bytes)
        except:
            print("LOGIN FAILURE!")
            exit(1)

    def receive(self):
        if self.username == "!dev-game-only":
            return
        while self.run.is_set():
            try:
                header = int.from_bytes(self.server.recv(1), "big")

                match header:
                    case 1:
                        self.chat.add_to_history("GAME_IN_PROGRESS")
                        if not self.game_in_progress.is_set():
                            raise Exception("Internal error, game should be running")

                        game_end = int.from_bytes(self.server.recv(8), "big")
                        game_end -= int(tm.time())

                        self.chat.add_to_history("game ends in: " + str(game_end) + " seconds")
                    case 2:
                        if self.is_drawing:
                            raise Exception("Received unknown data")
                        canvas_serialized = self.server.recv(CANVAS_SIZE_SERIALIZED)
                        self.canvas.unpack_and_set(canvas_serialized)
                    case 3:
                        self.chat.add_to_history("CHAT")

                        msg_size = int.from_bytes(self.server.recv(4), "big")
                        message = self.server.recv(msg_size).decode('ascii')
                        self.chat.add_to_history(message)
                    case 4:
                        self.chat.add_to_history("START_AND_GUESS")

                        game_end = int.from_bytes(self.server.recv(8), "big")
                        game_end -= int(tm.time())
                        self.chat.add_to_history("game ends in: " + str(game_end) + " seconds")

                        self.is_drawing.clear()
                        self.game_in_progress.set()
                    case 5:
                        self.chat.add_to_history("START_AND_DRAW")

                        msg_size = int.from_bytes(self.server.recv(4), "big")
                        message = self.server.recv(msg_size).decode('ascii')
                        self.chat.add_to_history(message)

                        game_end = int.from_bytes(self.server.recv(8), "big")
                        game_end -= int(tm.time())
                        self.chat.add_to_history("game ends in: " + str(game_end) + " seconds")

                        self.is_drawing.set()
                        self.game_in_progress.set()
                    case 6:
                        self.chat.add_to_history("INPUT_USERNAME")
                    case 7:
                        self.chat.add_to_history("CORRECT_GUESS")
                        self.correct_guess.set()
                    case 8:
                        self.chat.add_to_history("WRONG_GUESS")
                    case 9:
                        self.chat.add_to_history("CORRECT_GUESS_ANNOUNCEMENT")

                        msg_size = int.from_bytes(self.server.recv(4), "big")
                        message = self.server.recv(msg_size).decode('ascii')

                        self.chat.add_to_history(message)
                    case 10:
                        self.chat.add_to_history("INVALID_USERNAME")
                    case 11:
                        self.chat.add_to_history("WAITING_FOR_PLAYERS")

                        now_players = int.from_bytes(self.server.recv(4), "big")
                        need_players = int.from_bytes(self.server.recv(4), "big")

                        self.chat.add_to_history(
                            "waiting for players: (" + str(now_players) + "/" + str(need_players) + ")")
                    case 12:
                        self.chat.add_to_history("GAME_ENDS")
                        self.game_in_progress.clear()
                        self.correct_guess.clear()
                    case 13:
                        self.chat.add_to_history("SERVER_ERROR")  # todo: handle this...
                    case _:
                        print("[ERROR]: unknown header: ", header)
                        exit(1)
            except socket.timeout:
                continue
            except Exception as e:
                print("An error occurred!")
                print(e)
                self.server.close()
                break

    def send_guess(self, guess):
        if self.username == "!dev-game-only":
            return
        try:
            my_bfr = bytearray([3])
            my_bfr += len(guess).to_bytes(4, "big")
            my_bfr += bytearray(guess, "ascii")
            self.server.send(my_bfr)
        except Exception as e:
            print(e)
            exit(1)

    def send_canvas(self):
        if self.username == "!dev-game-only":
            return
        try:
            my_bfr = bytearray([2])
            my_bfr += self.canvas.grid_serialized.tobytes()
            self.server.send(my_bfr)
        except Exception as e:
            print(e)
            exit(1)
