import socket
import threading
import time as tm

nickname = input("Choose a nickname: ")
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('127.0.0.1', 9034))
    my_bytes = bytearray([6])
    print(my_bytes)
    my_bytes += len(nickname).to_bytes(4, "big")
    print(my_bytes)
    my_bytes += bytearray(nickname, "ascii")
    print(my_bytes)
    server.send(my_bytes)
except:
    print("FAILURE!")
    exit(1)


def receive():
    while True:
        try:
            header = int.from_bytes(server.recv(1), "big")

            match header:
                case 1:
                    print("GAME_IN_PROGRESS")
                    game_end = int.from_bytes(server.recv(8), "big")
                    game_end -= int(tm.time())
                    print("game ends in: " + str(game_end) + " seconds")
                case 2:
                    print("CANVAS")
                case 3:
                    print("CHAT")
                    msg_size = int.from_bytes(server.recv(4), "big")
                    message = server.recv(msg_size).decode('ascii')
                    print(message)
                case 4:
                    print("START_AND_GUESS")
                    game_end = int.from_bytes(server.recv(8), "big")
                    game_end -= int(tm.time())
                    print("game ends in: " + str(game_end) + " seconds")
                case 5:
                    print("START_AND_DRAW")

                    msg_size = int.from_bytes(server.recv(4), "big")
                    message = server.recv(msg_size).decode('ascii')
                    print(message)

                    game_end = int.from_bytes(server.recv(8), "big")
                    game_end -= int(tm.time())
                    print("game ends in: " + str(game_end) + " seconds")
                case 6:
                    print("INPUT_USERNAME")
                case 7:
                    print("CORRECT_GUESS")
                case 8:
                    print("WRONG_GUESS")
                case 9:
                    print("CORRECT_GUESS_ANNOUNCEMENT")
                    msg_size = int.from_bytes(server.recv(4), "big")
                    message = server.recv(msg_size).decode('ascii')
                    print(message)
                case 10:
                    print("INVALID_USERNAME")
                case 11:
                    print("WAITING_FOR_PLAYERS")
                    now_players = int.from_bytes(server.recv(4), "big")
                    need_players = int.from_bytes(server.recv(4), "big")
                    print("waiting for players: (" + str(now_players) + "/" + str(need_players) + ")")
                case 12:
                    print("GAME_ENDS")
                case 13:
                    print("SERVER_ERROR")
                case _:
                    print("[ERROR]: unknown header")
                    exit(1)
        except:
            print("An error occurred!")
            server.close()
            break


def send():
    while True:
        message = input("")
        my_bfr = bytearray([3])
        my_bfr += len(message).to_bytes(4, "big")
        my_bfr += bytearray(message, "ascii")
        server.send(my_bfr)


receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
