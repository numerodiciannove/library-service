from payments_app.models import Payment
from payments_app.serializers import PaymentSerializer
from rest_framework.viewsets import ModelViewSet


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Payment.objects.all()
        return Payment.objects.filter(borrowing_id=user.pk)
