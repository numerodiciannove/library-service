from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from books_app.models import Book
from borrowings_app.models import Borrowing

BORROWING_URL = reverse("borrowings:borrowing-list")


def sample_borrowing(user, book, borrow_date, expected_return_date):
    return Borrowing.objects.create(
        user=user,
        book=book,
        borrow_date=borrow_date,
        expected_return_date=expected_return_date
    )


class BorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com", password="testpassword"
        )

        self.book = Book.objects.create(
            title="Book",
            author="Author",
            inventory=1,
            daily_fee=10.00,
        )
        self.url = reverse("borrowings:borrowing-list")
        self.client.force_authenticate(user=self.user)

    def test_create_borrowing(self):
        borrow_date = datetime.now().date()
        expected_return_date = borrow_date + timedelta(days=3)
        data = {
            "borrow_date": borrow_date,
            "expected_return_date": expected_return_date,
            "book": self.book.pk,
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 1)

    def test_list_borrowings_by_user(self):
        borrow_date = datetime.now().date()
        expected_return_date = borrow_date + timedelta(days=3)
        sample_borrowing(
            user=self.user,
            book=self.book,
            borrow_date=borrow_date,
            expected_return_date=expected_return_date
        )

        url = reverse("borrowings:borrowing-list")
        response = self.client.get(
            url, {"user_id": self.user.id}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_all_borrowings_as_superuser(self):
        borrow_date = datetime.now().date()
        expected_return_date = borrow_date + timedelta(days=3)
        sample_borrowing(
            user=self.user,
            book=self.book,
            borrow_date=borrow_date,
            expected_return_date=expected_return_date
        )

        superuser = get_user_model().objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )
        self.client.force_authenticate(user=superuser)

        url = reverse("borrowings:borrowing-list")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_borrowings_by_title(self):
        borrow_date = datetime.now().date()
        expected_return_date = borrow_date + timedelta(days=3)
        borrowing = sample_borrowing(
            user=self.user,
            book=self.book,
            borrow_date=borrow_date,
            expected_return_date=expected_return_date
        )

        url = reverse("borrowings:borrowing-list")
        response = self.client.get(
            url, {"title": self.book.title}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], borrowing.id)
