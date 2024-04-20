from rest_framework import serializers
from books_app.models import Book


class BookSerializer(serializers.Serializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_fee",
        )
