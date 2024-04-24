from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from borrowings_app.models import Borrowing
from borrowings_app.serializers import (
    BorrowingSerializer,
    BorrowingRetrieveSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(ModelViewSet):
    queryset = Borrowing.objects.all()
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
