from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from books_app.models import Book

BOOK_URL = reverse("books_app:book-list")


def detail_url(book_id):
    return reverse("books_app:book-detail", args=[book_id])


def sample_book(**params):
    defaults = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "cover": "HARD",
        "inventory": 100,
        "daily_fee": 9.99,
    }
    defaults.update(**params)
    return Book.objects.create(**defaults)


class AdminBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@testmail.com", "testpassword", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.book = sample_book()
        self.url = detail_url(self.book.id)

    def test_create_book(self):
        payload = {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "cover": "SOFT",
            "inventory": 50,
            "daily_fee": 12.99,
        }
        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=response.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(book, key))

    def test_put_book(self):
        payload = {
            "title": "1984",
            "author": "George Orwell",
            "cover": "HARD",
            "inventory": 30,
            "daily_fee": 11.99,
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(self.book, key))

    def test_patch_book(self):
        payload = {
            "title": "Brave New World",
            "author": "Aldous Huxley",
        }
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(self.book, key))

    def test_delete_book(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
