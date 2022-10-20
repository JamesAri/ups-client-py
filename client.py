import socket
import threading
import time as tm
from model import Chat, Canvas
from utils import Timer

from settings import *


class Client:
    server: socket

    username: str
    chat: Chat
    canvas: Canvas
    timer: Timer

    run: threading.Event
    is_drawing: threading.Event
    game_in_progress: threading.Event
    correct_guess: threading.Event
    can_play: threading.Event

    def __init__(self, username: str):
        self.username = username

        self.chat = Chat()
        self.canvas = Canvas()
        self.timer = Timer()

        self.is_drawing = threading.Event()
        self.game_in_progress = threading.Event()
        self.correct_guess = threading.Event()
        self.can_play = threading.Event()
        self.run = threading.Event()

        self.run.set()

    def login(self):
        if self.username == "!dev-game-only":
            return
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(('127.0.0.1', 9034))
            self.server.settimeout(TIMEOUT_SEC)

            login_bfr = bytearray([6])
            login_bfr += len(self.username).to_bytes(4, "big")
            login_bfr += bytearray(self.username, "ascii")
            self.server.send(login_bfr)
        except Exception as ex:
            print(ex)
            print("LOGIN FAILURE!")
            exit(1)

    def receive(self):
        if self.username == "!dev-game-only":
            return
        while self.run.is_set():
            try:
                header = int.from_bytes(self.server.recv(1), "big")

                match header:
                    case 0:
                        print("Server hung up")
                        exit(1)
                    case 1:
                        self.chat.add_to_history(("GAME_IN_PROGRESS", SERVER_MESSAGE_COLOR))
                        drawing_flag = int.from_bytes(self.server.recv(1), "big")

                        if drawing_flag == 5:
                            guess_word_len = int.from_bytes(self.server.recv(4), "big")
                            guess_word = self.server.recv(guess_word_len).decode('ascii')
                            self.chat.add_to_history((guess_word, SERVER_MESSAGE_COLOR))

                        game_end = int.from_bytes(self.server.recv(8), "big")
                        canvas_serialized = self.recv_all(self.server, CANVAS_SIZE_SERIALIZED)

                        if drawing_flag == 5:
                            self.is_drawing.set()
                        self.timer.set_round_end(game_end)
                        self.canvas.unpack_and_set(canvas_serialized)
                        self.game_in_progress.set()
                        self.can_play.set()
                    case 2:
                        if self.is_drawing.is_set():
                            raise Exception("Received unknown data")
                        diffs_count = int.from_bytes(self.server.recv(4), "big")
                        diffs = []
                        for _ in range(diffs_count):
                            diffs.append(int.from_bytes(self.server.recv(4), "big"))
                        while diffs:
                            self.canvas.set_pixel_by_index(diffs.pop())
                    case 3:
                        self.chat.add_to_history(("CHAT", SERVER_MESSAGE_COLOR))

                        msg_size = int.from_bytes(self.server.recv(4), "big")
                        message = self.server.recv(msg_size).decode('ascii')
                        self.chat.add_to_history((message, GRAY))
                    case 4:
                        self.chat.add_to_history(("START_AND_GUESS", SERVER_MESSAGE_COLOR))

                        round_end = int.from_bytes(self.server.recv(8), "big")

                        self.timer.set_round_end(round_end)
                        self.is_drawing.clear()
                        self.game_in_progress.set()
                    case 5:
                        self.chat.add_to_history(("START_AND_DRAW", SERVER_MESSAGE_COLOR))

                        msg_size = int.from_bytes(self.server.recv(4), "big")
                        message = self.server.recv(msg_size).decode('ascii')
                        round_end = int.from_bytes(self.server.recv(8), "big")

                        self.chat.add_to_history((message, SERVER_MESSAGE_COLOR))

                        self.timer.set_round_end(round_end)
                        self.is_drawing.set()
                        self.game_in_progress.set()
                    case 6:
                        raise Exception("Invalid socket header")
                    case 7:
                        self.chat.add_to_history(("CORRECT_GUESS", CORRECT_ANSWER_COLOR))
                        self.correct_guess.set()
                    case 8:
                        self.chat.add_to_history(("WRONG_GUESS", SERVER_MESSAGE_COLOR))
                    case 9:
                        self.chat.add_to_history(("CORRECT_GUESS_ANNOUNCEMENT", SERVER_MESSAGE_COLOR))

                        msg_size = int.from_bytes(self.server.recv(4), "big")
                        message = self.server.recv(msg_size).decode('ascii')

                        self.chat.add_to_history((message, SERVER_MESSAGE_COLOR))
                    case 10:
                        self.chat.add_to_history(("INVALID_USERNAME", SERVER_MESSAGE_COLOR))
                    case 11:
                        self.chat.add_to_history(("WAITING_FOR_PLAYERS", SERVER_MESSAGE_COLOR))

                        now_players = int.from_bytes(self.server.recv(4), "big")
                        need_players = int.from_bytes(self.server.recv(4), "big")
                        msg = "waiting for players: (" + str(now_players) + "/" + str(need_players) + ")"
                        self.chat.add_to_history((msg, SERVER_MESSAGE_COLOR))
                    case 12:
                        self.chat.add_to_history(("GAME_ENDS", SERVER_MESSAGE_COLOR))
                        self.game_in_progress.clear()
                        self.correct_guess.clear()
                        self.timer.clear_round()
                        self.canvas.clear()
                    case 13:
                        self.chat.add_to_history(("SERVER_ERROR", SERVER_MESSAGE_COLOR))  # todo: handle this...
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

    @staticmethod
    def recv_all(sock, n):
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                raise Exception("recv_all err")
            data.extend(packet)
        return data

    def send_guess(self, guess: str):
        if self.username == "!dev-game-only":
            return
        if not self.can_play.is_set():
            return
        if self.is_drawing.is_set():
            return
        if not guess or guess.isspace():
            return
        try:
            my_bfr = bytearray([3])
            my_bfr += len(guess).to_bytes(4, "big")
            my_bfr += bytearray(guess, "ascii")
            self.server.send(my_bfr)
        except Exception as e:
            print(e)
            exit(1)

    def send_canvas_diff(self, queue: list):
        # queue -> (col, row)
        if self.username == "!dev-game-only":
            return
        if not self.can_play.is_set():
            return
        if not self.is_drawing.is_set():
            return
        try:
            my_bfr = bytearray([2])
            my_bfr += len(queue).to_bytes(4, "big")
            while queue:
                cords = queue.pop()
                my_bfr += (cords[0] * ROWS + cords[1]).to_bytes(4, "big")
            self.server.send(my_bfr)
        except Exception as e:
            print(e)
            exit(1)
