import os

import requests
from dotenv import load_dotenv
from typing import List
from borrowings_app.models import Borrowing
from django.utils import timezone

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


def get_overdue_borrowings() -> List[Borrowing]:
    current_date = timezone.now().date()
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=current_date,
        actual_return_date__isnull=True
    )
    return overdue_borrowings


def generate_message(borrowing: Borrowing) -> str:
    return (
        f"Dear {borrowing.user.email} - "
        f"🤓{borrowing.user.first_name} {borrowing.user.last_name}\n\n"
        f"This is a gentle reminder that you have not yet returned the book:"
        f"\n\n📘{borrowing.book.title}\n\n"
        f"Borrowed from the library.\n"
        f"We kindly ask you to return the book at your earliest convenience so "
        f"that other users may also benefit from it.\n \n"
        f"Thank you for your understanding and cooperation!\n \n"
        f"Best regards,\n"
        f"Library Administration"
    )


def generate_all_borrowing_messages() -> List[str]:
    overdue_borrowings = get_overdue_borrowings()
    messages = [generate_message(borrowing) for borrowing in overdue_borrowings]
    return messages
