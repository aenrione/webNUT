import requests
from .notifier import NotificationBuilder

class TelegramBuilder(NotificationBuilder):
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.message = None

    def is_valid(self):
        return self.bot_token and self.chat_id

    def set_message(self, message):
        self.message = message

    def send(self):
        if self.message:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': self.message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print("Notification sent successfully")
            else:
                print(f"Failed to send notification: {response.text}")

