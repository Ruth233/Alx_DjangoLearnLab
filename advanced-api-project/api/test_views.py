from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book


class BookAPITests(APITestCase):
    """Unit tests for Book API endpoints: CRUD + filters/search/order + permissions"""

    def setUp(self):
        # Create a user for authenticated requests
        self.user = User.objects.create_user(username="tester", password="pass1234")

        # Create some initial books
        self.book1 = Book.objects.create(
            title="Django Basics", author="Alice", publication_year=2021
        )
        self.book2 = Book.objects.create(
            title="Advanced Django", author="Bob", publication_year=2022
        )

        # Endpoints
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = reverse("book-detail", args=[self.book1.id])
        self.update_url = reverse("book-update", args=[self.book1.id])
        self.delete_url = reverse("book-delete", args=[self.book1.id])

    # ---------- Read / List ----------
    def test_list_books_public(self):
        """Anyone can list books"""
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_detail_book_public(self):
        """Anyone can retrieve a single book"""
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], self.book1.title)

    # ---------- Create ----------
    def test_create_book_requires_authentication(self):
        """Unauthenticated users cannot create"""
        payload = {"title": "New Book", "author": "Jane", "publication_year": 2023}
        res = self.client.post(self.create_url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        self.client.login(username="tester", password="pass1234")
        payload = {"title": "New Book", "author": "Jane", "publication_year": 2023}
        res = self.client.post(self.create_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="New Book").exists())

    # ---------- Update ----------
    def test_update_book_requires_authentication(self):
        payload = {"title": "Updated"}
        res = self.client.patch(self.update_url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        self.client.login(username="tester", password="pass1234")
        payload = {"title": "Updated Title"}
        res = self.client.patch(self.update_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    # ---------- Delete ----------
    def test_delete_book_requires_authentication(self):
        res = self.client.delete(self.delete_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        self.client.login(username="tester", password="pass1234")
        res = self.client.delete(self.delete_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
