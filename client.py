import socket
import threading

from settings import *
from model import Chat, Canvas
from utils import Timer

HEADER_SIZE = 1
INT_SIZE = 4
TIME_SIZE = 8


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

    def __init__(self, username: str):
        self.username = username

        self.chat = Chat()
        self.canvas = Canvas()
        self.timer = Timer()

        self.is_drawing = threading.Event()
        self.game_in_progress = threading.Event()
        self.correct_guess = threading.Event()
        self.run = threading.Event()

        self.run.set()

    def recv_all(self, size) -> bytearray:
        data = bytearray()
        while len(data) < size:
            packet = self.server.recv(size - len(data))
            if not packet:
                raise Exception("recv_all err")
            data.extend(packet)
        return data

    def recv_bytes(self, size: int) -> bytearray:
        return self.recv_all(size)

    def recv_header(self) -> int:
        return int.from_bytes(self.server.recv(HEADER_SIZE), "big")

    def recv_int(self) -> int:
        return int.from_bytes(self.recv_all(INT_SIZE), "big")

    def recv_time(self) -> int:
        return int.from_bytes(self.recv_all(TIME_SIZE), "big")

    def recv_msg(self, forward: bool = False) -> str:
        msg_len = self.recv_int()
        msg = self.recv_all(msg_len).decode('ascii')
        if forward:
            self.chat.add_to_history((msg, SERVER_MESSAGE_COLOR))
        return msg

    def login(self):
        if self.username == "!dev-game-only":
            return
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(('127.0.0.1', PORT))
            self.server.settimeout(TIMEOUT_SEC)

            login_bfr = bytearray([SocketHeader.INPUT_USERNAME])
            login_bfr += len(self.username).to_bytes(INT_SIZE, "big")
            login_bfr += bytearray(self.username, "ascii")
            self.server.send(login_bfr)
        except Exception as ex:
            print(ex)
            print("LOGIN FAILURE!\nChange your username.")
            exit(1)

    def receive(self):
        if self.username == "!dev-game-only":
            return
        while self.run.is_set():
            try:
                header = self.recv_header()

                match header:
                    case SocketHeader.EMPTY:
                        print("Server hung up")
                        break

                    case SocketHeader.GAME_IN_PROGRESS:
                        self.chat.add_to_history(("Joined game in progress", SERVER_MESSAGE_COLOR))

                        if self.recv_header() == SocketHeader.START_AND_DRAW:
                            self.chat.add_to_history((f"Draw: {self.recv_msg()}", ORANGE))
                            self.is_drawing.set()
                        else:
                            self.chat.add_to_history((f"Guess the object!", ORANGE))

                        game_end = self.recv_time()
                        canvas_serialized = self.recv_bytes(CANVAS_SIZE_SERIALIZED)

                        self.timer.set_round_end(game_end)
                        self.canvas.unpack_and_set(canvas_serialized)
                        self.game_in_progress.set()

                    case SocketHeader.CANVAS:
                        if self.is_drawing.is_set():
                            raise Exception("Received unknown data")

                        diffs_count = self.recv_int()
                        diffs = []

                        for _ in range(diffs_count):
                            diffs.append(self.recv_int())

                        while diffs:
                            self.canvas.set_pixel_by_index(diffs.pop())

                    case SocketHeader.CHAT:
                        msg = self.recv_msg()
                        self.chat.add_to_history((msg, GRAY))

                    case SocketHeader.START_AND_GUESS:
                        self.chat.add_to_history((f"Guess the drawing!", ORANGE))

                        round_end = self.recv_time()

                        self.timer.set_round_end(round_end)
                        self.is_drawing.clear()
                        self.game_in_progress.set()

                    case SocketHeader.START_AND_DRAW:
                        self.chat.add_to_history((f"Draw: {self.recv_msg()}", ORANGE))

                        round_end = self.recv_time()

                        self.timer.set_round_end(round_end)
                        self.is_drawing.set()
                        self.game_in_progress.set()

                    case SocketHeader.INPUT_USERNAME:
                        raise Exception("Invalid socket header")

                    case SocketHeader.CORRECT_GUESS:
                        self.chat.add_to_history(("That's correct!", CORRECT_ANSWER_COLOR))
                        self.correct_guess.set()
                        self.timer.can_play.clear()

                    case SocketHeader.WRONG_GUESS:
                        self.chat.add_to_history(("Wrong guess", SERVER_MESSAGE_COLOR))

                    case SocketHeader.CORRECT_GUESS_ANNOUNCEMENT:
                        self.recv_msg(forward=True)

                    case SocketHeader.INVALID_USERNAME:
                        self.chat.add_to_history(("Invalid username!", SERVER_MESSAGE_COLOR))

                    case SocketHeader.WAITING_FOR_PLAYERS:
                        now_players = self.recv_int()
                        need_players = self.recv_int()

                        msg = f"Waiting for players to join ({now_players}/{need_players})"
                        self.chat.add_to_history((msg, SERVER_MESSAGE_COLOR))

                    case SocketHeader.GAME_ENDS:
                        self.chat.clear_history()
                        self.game_in_progress.clear()
                        self.correct_guess.clear()
                        self.timer.clear_round()
                        self.canvas.clear()

                    case SocketHeader.SERVER_ERROR:
                        self.chat.add_to_history(("SERVER_ERROR", SERVER_MESSAGE_COLOR))
                        break

                    case _:
                        print("[ERROR]: Unknown header: ", header)
                        break
            except socket.timeout:
                continue
            except Exception as e:
                print("An error occurred!")
                print(e)
                self.server.close()
                break

    def send_guess(self, guess: str):
        if self.username == "!dev-game-only":
            return
        if not self.timer.can_play.is_set():
            return
        if self.is_drawing.is_set():
            return
        if not guess or guess.isspace():
            return
        try:
            my_bfr = bytearray([SocketHeader.CHAT])
            my_bfr += len(guess).to_bytes(INT_SIZE, "big")
            my_bfr += bytearray(guess, "ascii")
            self.server.send(my_bfr)
        except Exception as e:
            print(e)

    def send_canvas_diff(self, queue: list):
        if self.username == "!dev-game-only":
            return
        if not self.timer.can_play.is_set():
            return
        if not self.is_drawing.is_set():
            return
        try:

            my_bfr = bytearray([SocketHeader.CANVAS])
            my_bfr += len(queue).to_bytes(INT_SIZE, "big")
            while queue:
                col, row = queue.pop()
                index = col * ROWS + row
                my_bfr += index.to_bytes(INT_SIZE, "big")
            self.server.send(my_bfr)
        except Exception as e:
            print(e)
