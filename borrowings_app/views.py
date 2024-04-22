from borrowings_app.models import Borrowing
from borrowings_app.serializers import BorrowSerializer, BorrowRetrieveSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class BorrowingViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowRetrieveSerializer

        return BorrowSerializer
