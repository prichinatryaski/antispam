import logging

class TelegramHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()

    def emit(self, message, bot):
        try:
            log_entry = self.format(text)
            self.bot.send_message(chat_id=self.chat_id, text=log_entry)
        except TelegramError as e:
            print(f"Failed to send log to Telegram: {e}")