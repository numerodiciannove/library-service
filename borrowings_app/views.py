from rest_framework.viewsets import ModelViewSet
from borrowings_app.models import Borrowing
from borrowings_app.serializers import (
    BorrowSerializer,
    BorrowRetrieveSerializer,
    BorrowCreateSerializer,
)


class BorrowingViewSet(ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowRetrieveSerializer
        if self.action == "create":
            return BorrowCreateSerializer

        return BorrowSerializer
