class Chat:
    old_texts: [str] = []
    current_text: str = ''

    def use_backspace(self):
        self.current_text = self.current_text[:-1]
