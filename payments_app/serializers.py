from payments_app.models import Payment
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentBorrowingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status",
            "session_url"
        )


class PaymentBorrowingRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status",
            "type",
            "session_url",
            "session_id",
            "money_to_pay",
        )
