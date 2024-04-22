from books_app.models import Book
from books_app.serializers import BookSerializer
from django.db import transaction
from rest_framework import serializers
from borrowings_app.models import Borrowing
from users_app.serializers import UserSerializer


class BorrowSerializer(serializers.ModelSerializer):
    user = serializers.EmailField()
    book = serializers.CharField()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowRetrieveSerializer(BorrowSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)


class BorrowCreateSerializer(BorrowSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    def validate(self, data):
        if data["expected_return_date"] < data["borrow_date"]:
            raise serializers.ValidationError(
                "Expected return date must be after borrow date"
            )
        return data

    def validate_book(self, value):
        book = value
        if book.inventory == 0:
            raise serializers.ValidationError(
                "Book is not available for borrowing"
            )
        return book

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data["book"]
            borrow_date = validated_data.pop("borrow_date")
            expected_return_date = validated_data.pop("expected_return_date")
            user = self.context["request"].user

            borrowing = Borrowing.objects.create(
                book=book,
                user=user,
                expected_return_date=expected_return_date,
                borrow_date=borrow_date,
            )
            book.inventory -= 1
            book.save()
            return borrowing

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
        )
