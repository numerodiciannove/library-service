from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users_app.views import CreateUserView, ManageUserView

urlpatterns = [
    path("", CreateUserView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "me/",
        ManageUserView.as_view(
            actions={"get": "retrieve", "put": "update"}
        ),
        name="manage"
    ),
]

app_name = "user"
