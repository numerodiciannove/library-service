from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from borrowings_app.models import Borrowing
from borrowings_app.serializers import (
    BorrowingSerializer,
    BorrowingRetrieveSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(ModelViewSet):
    queryset = Borrowing.objects.select_related("user", "book").all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def get_filtered_queryset(self, request):
        """
        Filters the queryset based on user_id and/or is_active parameters
        in the request query string.
        """
        queryset = self.queryset

        user_id = request.query_params.get("user_id")
        is_active = request.query_params.get("is_active")

        if not request.user.is_staff:
            queryset = queryset.filter(user=request.user)

        if user_id:
            queryset = self._filter_by_user(queryset, user_id)

        if is_active is not None:
            queryset = self._filter_by_activity(queryset, is_active)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter borrowing what's currently active",
            ),
            OpenApiParameter(
                name="user_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="See other users borrowings if you are admin",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Get a list of borrowings with optional filtering.

        This method returns a list of borrowings optionally filtered by user_id
        and/or is_active parameters in the query string. Non-admin users
        can only see their own borrowings.
        """
        queryset = self.get_filtered_queryset(request)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

    @staticmethod
    def _filter_by_user(queryset, user_id):
        """
        Filter the queryset by user_id.
        """
        return queryset.filter(user_id=user_id)

    @staticmethod
    def _filter_by_activity(queryset, is_active):
        """
        This method filters the queryset by the provided is_active parameter.
        """
        is_active = is_active.lower() == "true"
        return queryset.filter(actual_return_date__isnull=is_active)
