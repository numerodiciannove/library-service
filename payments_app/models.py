from django.db import models


class Payment(models.Model):
    class PayStatus(models.TextChoices):
        PENDING = "PENDING"
        PAID = "PAID"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT"
        FINE = "FINE"

    status = models.CharField(max_length=19, choices=PayStatus)
    type = models.CharField(max_length=19, choices=Type)
    borrowing_id = models.IntegerField()
    session_url = models.URLField(max_length=255)
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return (
            f"Type: '{self.type}', "
            f"Status:'{self.status}', "
            f"Borrowing:{self.borrowing_id}"
        )
