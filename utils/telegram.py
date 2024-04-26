import os

import requests
from dotenv import load_dotenv

load_dotenv()


def message_sender(text_message: str) -> [dict, list]:
    telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]
    telegram_method = "sendMessage"

    response = requests.post(
        url="https://api.telegram.org/bot{0}/{1}".format(
            telegram_bot_token, telegram_method
        ),
        data={"chat_id": telegram_chat_id, "text": text_message},
    ).json()

    return response
