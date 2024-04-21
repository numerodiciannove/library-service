from django.contrib import admin
from django.urls import path, include

app_name = "users_app"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/books/", include("books_app.urls", namespace="books")),
    path("api/v1/users/", include("users_app.urls", namespace="users")),
]
