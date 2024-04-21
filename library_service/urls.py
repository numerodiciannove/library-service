from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

app_name = "users_app"

# Apps endpoints
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/books/", include("books_app.urls", namespace="books")),
    path("api/v1/users/", include("users_app.urls", namespace="users")),
]

# Swagger documentation
urlpatterns += [
    path("api/doc/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
