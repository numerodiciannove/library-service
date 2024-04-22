from rest_framework import routers
from django.urls import path, include
from borrowings_app.views import BorrowingViewSet

app_name = "borrowings_app"

router = routers.DefaultRouter()

router.register("", BorrowingViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
