import threading

from settings import MAX_MSG_LEN, HIST_BUFFER_SIZE


class Chat:
    history: [str] = []
    current_text: str = ''
    chat_lock: threading.Lock

    def __init__(self):
        self.chat_lock = threading.Lock()

    def use_backspace(self):
        self.current_text = self.current_text[:-1]

    def add_current_to_history(self):
        if len(self.current_text) > MAX_MSG_LEN:
            self.current_text = self.current_text[:MAX_MSG_LEN]
        self.add_to_history(self.current_text)
        self.current_text = ''

    def add_to_history(self, text: str):
        with self.chat_lock:
            if text.isspace() or not text:
                return
            if len(text) > MAX_MSG_LEN:
                return
            if len(self.history) >= HIST_BUFFER_SIZE:
                self.history.pop()
            self.history[:0] = [text]

    def clear_history(self):
        with self.chat_lock:
            self.history.clear()
