from django.db import models


class Book(models.Model):
    COVER_CHOICES = (
        ("HARD", "Hard"),
        ("SOFT", "Soft"),
    )

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=4,
        choices=COVER_CHOICES,
        default="HARD",
    )
    inventory = models.PositiveSmallIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("title", "author")

    def __str__(self):
        return f"{self.title} - {self.author}, available - {self.inventory}"
