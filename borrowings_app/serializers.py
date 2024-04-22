from books_app.serializers import BookSerializer
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
