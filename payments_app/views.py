from borrowings_app.models import Borrowing
from payments_app.models import Payment
from payments_app.serializers import PaymentSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class PaymentViewSet(ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Payment.objects.all()

        user_borrowings_ids = Borrowing.objects.filter(
            user=user
        ).values_list('id', flat=True)

        return Payment.objects.filter(borrowing_id__in=user_borrowings_ids)
