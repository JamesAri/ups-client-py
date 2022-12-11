from settings import *
from .handlers import ClientHandler
from model import Chat, Canvas
from utils import Timer, get_valid_username
import time as time

import socket
import threading

MAX_RECONNECT_DURATION = 30  # in seconds
SLEEP_RECONNECT_DURATION = 2  # in seconds


class Client:
    server: socket
    address: str
    port: int

    handler: ClientHandler

    username: str
    players: dict[str, bool]
    players_lock: threading.Lock

    chat: Chat
    canvas: Canvas
    timer: Timer

    run: threading.Event
    is_drawing: threading.Event
    game_in_progress: threading.Event
    correct_guess: threading.Event

    def __init__(self, username: str, address: str, port: int):
        self.address = address
        self.port = port

        self.handler = ClientHandler(self)

        self.online: bool = False
        self.username = username
        self.players = dict()
        self.players_lock = threading.Lock()

        self.chat = Chat()
        self.canvas = Canvas()
        self.timer = Timer()

        self.run = threading.Event()
        self.is_drawing = threading.Event()
        self.game_in_progress = threading.Event()
        self.correct_guess = threading.Event()

        self.run.set()

        if self.username == "!dev-game-only":
            self.update_players(self.username, False)
            self.timer.can_play.set()
            # self.is_drawing.set()  # toggle for drawing debug

    def update_players(self, key, val):
        with self.players_lock:
            self.players[key] = val

    def get_player_from_player_list(self, key):
        with self.players_lock:
            return self.players[key]

    def get_num_of_players(self):
        with self.players_lock:
            return len(self.players)

    def connect_to_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server.settimeout(TIMEOUT_SEC)
        self.server.connect((self.address, self.port))

    def login(self):
        if self.username == "!dev-game-only":
            return
        try:
            while not self.handler.handle_login_attempt():
                pass
            print("Login successful.")
        except Exception as e:
            print(f"Login error: {e}")
            self.handler.handle_server_close()

    def receive(self):
        if self.username == "!dev-game-only":
            return

        time_error = 0

        while self.run.is_set():
            try:
                if not self.online:
                    time.sleep(SLEEP_RECONNECT_DURATION)
                    if int(time.time()) - time_error > MAX_RECONNECT_DURATION:
                        print(f"Couldn't recover. Exiting.")
                        break
                    print(f"Attempting to reconnect")
                    if self.handler.handle_login_attempt():
                        print(f"You are back online!")
                    else:
                        continue

                header = self.handler.recv_header()

                match header:
                    case SocketHeader.DISCONNECTED:
                        self.handler.handle_disconnected()

                    case SocketHeader.GAME_IN_PROGRESS:
                        self.handler.handle_game_in_progress()

                    case SocketHeader.CANVAS:
                        self.handler.handle_canvas()

                    case SocketHeader.CHAT:
                        self.handler.handle_chat()

                    case SocketHeader.START_AND_GUESS:
                        self.handler.handle_start_and_guess()

                    case SocketHeader.START_AND_DRAW:
                        self.handler.handle_start_and_draw()

                    case SocketHeader.LOGIN:
                        self.handler.handle_login()

                    case SocketHeader.INVALID_USERNAME:
                        self.handler.handle_invalid_username()

                    case SocketHeader.CORRECT_GUESS:
                        self.handler.handle_correct_guess()

                    case SocketHeader.WRONG_GUESS:
                        self.handler.handle_wrong_guess()

                    case SocketHeader.CORRECT_GUESS_ANNOUNCEMENT:
                        self.handler.handle_correct_guess_announcement()

                    case SocketHeader.WAITING_FOR_PLAYERS:
                        self.handler.handle_waiting_for_players()

                    case SocketHeader.GAME_ENDS:
                        self.handler.handle_game_ends()

                    case SocketHeader.SERVER_ERROR:
                        self.handler.handle_server_error()

                    case SocketHeader.PLAYER_LIST:
                        self.handler.handle_player_list()

                    case SocketHeader.PLAYER_LIST_CHANGE:
                        self.handler.handle_player_list_change()

                    case SocketHeader.SERVER_FULL:
                        self.handler.handle_server_full()

                    case SocketHeader.HEARTBEAT:
                        self.handler.handle_heartbeat()

                    case _:
                        self.handler.handle_unknown_header()

            except socket.timeout:
                continue
            except Exception as e:
                if self.online:
                    time_error = int(time.time())
                    self.handler.handle_server_close()
                print(f"ERROR: {e}")
                continue

    def ready_to_send(self) -> bool:
        return self.online and self.timer.can_play.is_set()

    def send_guess(self, guess: str):
        if self.is_drawing.is_set() or not self.ready_to_send():
            return
        if not guess or guess.isspace():
            return
        try:
            self.handler.handle_send_guess(guess)
        except Exception as e:
            print(e)

    def send_canvas_diff(self, queue: list):
        if not self.is_drawing.is_set() or not self.ready_to_send():
            return
        try:
            self.handler.handle_send_canvas_diff(queue)
        except Exception as e:
            print(e)
