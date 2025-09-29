from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book


class BookAPITests(APITestCase):
    """Unit tests for Book API endpoints: CRUD + filters/search/order + permissions"""

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass1234")

        self.book1 = Book.objects.create(
            title="Django Basics", author="Alice", publication_year=2021
        )
        self.book2 = Book.objects.create(
            title="Advanced Django", author="Bob", publication_year=2022
        )

        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = reverse("book-detail", args=[self.book1.id])
        self.update_url = reverse("book-update", args=[self.book1.id])
        self.delete_url = reverse("book-delete", args=[self.book1.id])

    # ---------- Read / List ----------
    def test_list_books_public(self):
        """Anyone can list books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)   # <-- response.data

    def test_detail_book_public(self):
        """Anyone can retrieve a single book"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)  # <-- response.data

    # ---------- Create ----------
    def test_create_book_requires_authentication(self):
        payload = {"title": "New Book", "author": "Jane", "publication_year": 2023}
        response = self.client.post(self.create_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        self.client.login(username="tester", password="pass1234")
        payload = {"title": "New Book", "author": "Jane", "publication_year": 2023}
        response = self.client.post(self.create_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")  # <-- response.data

    # ---------- Update ----------
    def test_update_book_authenticated(self):
        self.client.login(username="tester", password="pass1234")
        payload = {"title": "Updated Title"}
        response = self.client.patch(self.update_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")  # <-- response.data

    # ---------- Delete ----------
    def test_delete_book_authenticated(self):
        self.client.login(username="tester", password="pass1234")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ---------- Filtering / Search / Ordering ----------
    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url, {"author": "Alice"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)   # <-- response.data
        self.assertEqual(response.data[0]["author"], "Alice")

    def test_search_books_by_title(self):
        response = self.client.get(self.list_url, {"search": "Advanced"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Advanced Django")

    def test_order_books_by_publication_year_desc(self):
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]  # <-- response.data
        self.assertEqual(years, sorted(years, reverse=True))

