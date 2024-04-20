from books_app.serializers import BookSerializer
from rest_framework.viewsets import ModelViewSet
from books_app.models import Book


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
