from books_app.models import Book
from django.db import models
from users_app.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_query_name="borrowings"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_query_name="borrowings"
    )

    class Meta:
        ordering = (
            "borrow_date",
            "expected_return_date",
        )

    def __str__(self):
        return (
            f"🤓{self.user.first_name} {self.user.last_name} "
            f"- borrows 📘{self.book.title} "
        )
