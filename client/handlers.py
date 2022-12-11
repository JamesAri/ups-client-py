import time

from settings import *
from utils import get_valid_username

HEADER_SIZE = 1
INT_SIZE = 4
TIME_SIZE = 8

RECONNECT_DUR = 5


class InvalidUsernameException(Exception):
    pass


class ClientHandler:

    def __init__(self, client):
        self.client = client

    ###############################################################

    def recv_all(self, size) -> bytearray:
        data = bytearray()
        while len(data) < size:
            packet = self.client.server.recv(size - len(data))
            if not packet:
                raise Exception("recv_all err")
            data.extend(packet)
        return data

    def recv_bytes(self, size: int) -> bytearray:
        return self.recv_all(size)

    def recv_header(self) -> int:
        return int.from_bytes(self.client.server.recv(HEADER_SIZE), "big")

    def recv_int(self) -> int:
        return int.from_bytes(self.recv_all(INT_SIZE), "big")

    def recv_time(self) -> int:
        return int.from_bytes(self.recv_all(TIME_SIZE), "big")

    def recv_msg(self, forward: bool = False) -> str:
        msg_len = self.recv_int()
        msg = self.recv_all(msg_len).decode('ascii')
        if forward:
            self.client.chat.add_to_history((msg, SERVER_MESSAGE_COLOR))
        return msg

    ###############################################################

    def handle_server_close(self):
        self.client.online = False
        self.client.update_players(self.client.username, self.client.online)
        self.client.server.close()
        self.client.chat.add_to_history(("An error occurred, you are offline now", SERVER_MESSAGE_COLOR))
        self.client.chat.add_to_history(("Check console for error details", SERVER_MESSAGE_COLOR))

    ###############################################################

    def handle_login_attempt(self) -> bool:
        self.client.connect_to_server()

        login_bfr = bytearray([SocketHeader.LOGIN])
        login_bfr += len(self.client.username).to_bytes(INT_SIZE, "big")
        login_bfr += bytearray(self.client.username, "ascii")
        self.client.server.send(login_bfr)

        hdr = self.recv_header()  # server response

        if hdr == SocketHeader.OK:
            self.client.online = True
            return True
        elif hdr == SocketHeader.INVALID_USERNAME:
            self.client.server.close()
            print("Login failure! Username already in use.")
            self.client.username = get_valid_username()
        elif hdr == SocketHeader.SERVER_FULL:
            self.client.server.close()
            print(f"Server full, reconnecting in {RECONNECT_DUR} seconds")
            time.sleep(RECONNECT_DUR)
        elif hdr == SocketHeader.DISCONNECTED:
            self.handle_disconnected()  # server disconnected us, we don't know why
        else:
            raise Exception(f"LOGIN ERROR: received unknown header during login (header: {hdr})")
        return False

    def handle_send_canvas_diff(self, queue: list):
        my_bfr = bytearray([SocketHeader.CANVAS])
        my_bfr += len(queue).to_bytes(INT_SIZE, "big")
        while queue:
            col, row = queue.pop()
            index = col * ROWS + row
            my_bfr += index.to_bytes(INT_SIZE, "big")
        self.client.server.send(my_bfr)  # TODO use sendall

    def handle_send_guess(self, guess: str):
        my_bfr = bytearray([SocketHeader.CHAT])
        my_bfr += len(guess).to_bytes(INT_SIZE, "big")
        my_bfr += bytearray(guess, "ascii")
        self.client.server.send(my_bfr)

    def handle_send_heartbeat(self):
        my_bfr = bytearray([SocketHeader.HEARTBEAT])
        self.client.server.send(my_bfr)

    ###############################################################
    def handle_unknown_header(self):
        raise Exception("Received invalid header")

    def handle_disconnected(self):
        raise Exception(
            "Disconnected by server (server hung up, crash dump generation in future app -> support, ticket, etc.)")

    def handle_ok(self):
        pass

    def handle_canvas(self):
        if self.client.is_drawing.is_set():
            raise Exception("Received unknown data")

        diffs_count = self.recv_int()

        diffs = []
        for _ in range(diffs_count):
            diffs.append(self.recv_int())

        while diffs:
            self.client.canvas.toggle_pixel_by_index(diffs.pop())

    def handle_chat(self):
        msg = self.recv_msg()
        self.client.chat.add_to_history((msg, GRAY))

    def handle_start_and_guess(self):
        self.client.chat.clear_input()
        self.client.chat.add_to_history((f"Guess the drawing!", ORANGE))

        round_end = self.recv_time()

        self.client.timer.set_round_end(round_end)
        self.client.is_drawing.clear()
        self.client.game_in_progress.set()
        self.client.canvas.clear()

    def handle_start_and_draw(self):
        self.client.chat.clear_input()
        self.client.chat.add_to_history((f"Draw: {self.recv_msg()}", ORANGE))

        round_end = self.recv_time()

        self.client.timer.set_round_end(round_end)
        self.client.is_drawing.set()
        self.client.game_in_progress.set()
        self.client.canvas.clear()

    def handle_login(self):
        raise Exception("Invalid socket header, login already completed")

    def handle_correct_guess(self):
        self.client.chat.add_to_history(("That's correct!", CORRECT_ANSWER_COLOR))
        self.client.correct_guess.set()
        self.client.timer.can_play.clear()

    def handle_wrong_guess(self):
        self.client.chat.add_to_history(("Wrong guess", SERVER_MESSAGE_COLOR))

    def handle_correct_guess_announcement(self):
        self.recv_msg(forward=True)

    def handle_invalid_username(self):
        raise Exception("Invalid socket header, login already completed")

    def handle_waiting_for_players(self):
        now_players = self.recv_int()
        need_players = self.recv_int()

        msg = f"Waiting for players to join ({now_players}/{need_players})"
        self.client.chat.add_to_history((msg, SERVER_MESSAGE_COLOR))

    def handle_game_ends(self):
        self.client.chat.clear_history()
        self.client.game_in_progress.clear()
        self.client.correct_guess.clear()
        self.client.timer.clear_round()
        self.client.canvas.clear()

    def handle_game_in_progress(self):
        self.client.chat.add_to_history(("Joined game in progress", SERVER_MESSAGE_COLOR))

        if self.recv_header() == SocketHeader.START_AND_DRAW:
            self.client.chat.add_to_history((f"Draw: {self.recv_msg()}", ORANGE))
            self.client.is_drawing.set()
        else:
            self.client.chat.add_to_history((f"Guess the object!", ORANGE))

        game_end = self.recv_time()
        canvas_serialized = self.recv_bytes(CANVAS_SIZE_SERIALIZED)

        self.client.timer.set_round_end(game_end)
        self.client.canvas.unpack_and_set(canvas_serialized)
        self.client.game_in_progress.set()

    def handle_server_error(self):
        raise Exception("There is some error on server side")

    def handle_player_list(self):
        num_of_players = self.recv_int()
        for _ in range(num_of_players):
            self.handle_player_list_change()

    def handle_player_list_change(self):
        username = self.recv_msg()
        status = int.from_bytes(self.recv_bytes(1), "big")
        self.client.update_players(username, bool(status))

    def handle_server_full(self):
        raise Exception("Player should be already in a game")

    def handle_heartbeat(self):
        print("♥")
        self.handle_send_heartbeat()
