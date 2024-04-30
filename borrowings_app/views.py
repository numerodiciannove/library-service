from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from borrowings_app.models import Borrowing
from borrowings_app.serializers import (
    BorrowingSerializer,
    BorrowingRetrieveSerializer,
    BorrowingCreateSerializer,
)
from utils.stripe_sessions import create_payment


class BorrowingViewSet(
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet
):
    queryset = Borrowing.objects.select_related("user", "book")
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",") if str_id]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def get_queryset(self):
        queryset = self.queryset
        is_active_param = self.request.query_params.get("is_active")
        user_id_param = self.request.query_params.get("user_id")

        if is_active_param:
            queryset = queryset.filter(actual_return_date=None)

        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        if user_id_param:
            user_ids = self._params_to_ints(user_id_param)
            queryset = queryset.filter(user__id__in=user_ids)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            borrowing = serializer.save()
            payment = create_payment(
                borrowing=borrowing,
                payment_type="PAYMENT",
            )
            borrowing.payments.add(payment)
            borrowing.save()

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {
                    "message": "You do not have permission to perform this action."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_active",
                type={"type": "list", "items": {"type": "any"}},
                description="Filter borrowings by status (eg. ?is_active=)",
            ),
            OpenApiParameter(
                "user_id",
                type={"type": "list", "items": {"type": "number"}},
                description=(
                    "Admin user ids filter "
                    "for borrowings (eg. ?user_id=1,3)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["POST"],
        url_path="return",
        permission_classes=[IsAdminUser, IsAuthenticated],
    )
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"message": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = timezone.now()
        borrowing.save()

        book = borrowing.book
        book.inventory += 1
        book.save()

        return Response(
            {"message": "Borrowing returned successfully."},
            status=status.HTTP_200_OK,
        )
