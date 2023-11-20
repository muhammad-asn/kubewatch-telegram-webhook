import os
import requests
import json

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_TOPIC_ID = os.getenv("TELEGRAM_TOPIC_ID")
TELEGRAM_URL = "https://api.telegram.org"

if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID and TELEGRAM_TOPIC_ID):
    raise EnvironmentError("The Telegram environment variables are not set.")


class Telegram:
    def __init__(self):
        self.telegram_bot_token = TELEGRAM_BOT_TOKEN
        self.telegram_chat_id = TELEGRAM_CHAT_ID
        self.telegram_topic_id = TELEGRAM_TOPIC_ID

    def send_message(self, message):
        msg = ""
        try:
            if message.eventmeta.reason == "Created":
                msg = f"""
✅ *Info: Resource Created* ✅            
*Name:* {message.eventmeta.name}
*Namespace:* {message.eventmeta.namespace}
*Reason:* {message.eventmeta.reason}
*Message:* {message.text}
        """

            elif message.eventmeta.reason == "Deleted":
                msg = f"""
🚨 *Alert: Resource Deleted* 🚨
*Name:* {message.eventmeta.name}
*Namespace:* {message.eventmeta.namespace}
*Reason:* {message.eventmeta.reason}
*Message:* {message.text}
        """

            data = {
                "chat_id": self.telegram_chat_id,
                "text": msg,
                "message_thread_id": self.telegram_topic_id,
                "parse_mode": "Markdown",
            }
            headers = {"Content-Type": "application/json"}
            requests.post(
                f"{TELEGRAM_URL}/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                headers=headers,
                data=json.dumps(data),
            )

        except Exception as e:
            print(f"Error sending message: {e}")
