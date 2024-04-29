from library_service.celery import app

from utils.telegram import message_sender, generate_all_borrowing_messages


@app.task()
def send_overdue_message():
    messages = generate_all_borrowing_messages()

    for message in messages:
        message_sender(message)
