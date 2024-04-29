from library_service.celery import app

from utils.overdue_borrowings_text_generator import (
    generate_all_borrowing_messages
)

from utils.telegram import message_sender


@app.task()
def send_overdue_message():
    messages = generate_all_borrowing_messages()

    for message in messages:
        message_sender(message)
