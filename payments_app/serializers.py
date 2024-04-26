from payments_app.models import Payment
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status",
            "type",
            "borrowing_id",
            "session_url",
            "session_id",
            "money_to_pay"
        )
