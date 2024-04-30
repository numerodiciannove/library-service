from borrowings_app.models import Borrowing
from django.db import models


class Payment(models.Model):
    class PayStatus(models.TextChoices):
        PENDING = "PENDING"
        PAID = "PAID"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT"
        FINE = "FINE"

    status = models.CharField(
        max_length=19,
        choices=PayStatus,
        default="PENDING"
    )
    type = models.CharField(
        max_length=19,
        choices=Type,
        default="PAYMENT"
    )
    borrowing = models.ForeignKey(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    session_url = models.URLField(max_length=255)
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Type: '{self.type}', " f"Status:'{self.status}'"
