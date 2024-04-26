from typing import List
from borrowings_app.models import Borrowing
from django.utils import timezone


def get_overdue_borrowings() -> List[Borrowing]:
    current_date = timezone.now().date()
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=current_date,
        actual_return_date__isnull=True
    )
    return overdue_borrowings


def generate_message(borrowing: Borrowing) -> str:
    return (
        f"Dear {borrowing.user.email} - 🤓{borrowing.user.first_name} {borrowing.user.last_name}\n\n"
        f"This is a gentle reminder that you have not yet returned the book:"
        f"\n\n📘{borrowing.book.title}\n\n"
        f"Borrowed from the library.\n"
        f"We kindly ask you to return the book at your earliest convenience so "
        f"that other users may also benefit from it.\n \n"
        f"Thank you for your understanding and cooperation!\n \n"
        f"Best regards,\n"
        f"Library Administration"
    )


def generate_all_messages() -> List[str]:
    overdue_borrowings = get_overdue_borrowings()
    messages = [generate_message(borrowing) for borrowing in overdue_borrowings]
    return messages
