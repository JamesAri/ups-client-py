from utils import MAX_CHAR


class Chat:
    history: [str] = []
    current_text: str = ''

    def __init__(self, history_buffer_limit):
        self.history_buffer_limit = history_buffer_limit

    def use_backspace(self):
        self.current_text = self.current_text[:-1]

    def add_current_to_history(self):
        if len(self.current_text) > MAX_CHAR:
            self.current_text = self.current_text[:MAX_CHAR]
        self.add_to_history(self.current_text)
        self.current_text = ''

    def add_to_history(self, text: str):
        if text.isspace() or not text:
            return
        if len(text) > MAX_CHAR:
            return
        if len(self.history) >= self.history_buffer_limit:
            self.history.pop()
        self.history[:0] = [text]

    def clear_history(self):
        self.history.clear()
