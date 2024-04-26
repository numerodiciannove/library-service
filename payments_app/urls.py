from payments_app.views import PaymentViewSet
from rest_framework import routers
from django.urls import path, include

app_name = "payments_app"

router = routers.DefaultRouter()

router.register("", PaymentViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
