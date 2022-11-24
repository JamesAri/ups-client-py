# SHARED DEFINITIONS:
# Future application can use settings (json-xml like) file or describe
# some of these definitions in a protocol.

from enum import IntEnum

ROWS = COLS = 100

ROUND_DUR_SEC = 60

MAX_USERNAME_LEN = 14
MAX_GUESS_LEN = 15

PORT = 9034


class SocketHeader(IntEnum):
    DISCONNECTED = 0
    OK = 1
    CANVAS = 2
    CHAT = 3
    START_AND_GUESS = 4
    START_AND_DRAW = 5
    LOGIN = 6
    CORRECT_GUESS = 7
    WRONG_GUESS = 8
    CORRECT_GUESS_ANNOUNCEMENT = 9
    INVALID_USERNAME = 10
    WAITING_FOR_PLAYERS = 11
    GAME_ENDS = 12
    GAME_IN_PROGRESS = 13
    SERVER_ERROR = 14
    PLAYER_LIST = 15
    PLAYER_LIST_CHANGE = 16
    SERVER_FULL = 17
