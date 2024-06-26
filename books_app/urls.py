from rest_framework import routers
from django.urls import path, include
from books_app.views import BookViewSet

app_name = "books_app"

router = routers.DefaultRouter()

router.register("", BookViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
