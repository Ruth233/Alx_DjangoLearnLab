# api/test_views.py
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


class BookAPITestCase(APITestCase):
    """
    Tests CRUD, filtering, search, ordering and permissions for Book endpoints.
    """

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='testuser', password='pass123')
        # Seed some books
        self.book1 = Book.objects.create(title="Django Unchained", author="Tarantino", publication_year=2012)
        self.book2 = Book.objects.create(title="Python 101", author="Guido", publication_year=2020)
        self.book3 = Book.objects.create(title="API Design", author="Guido", publication_year=2023)

        # Common URLs
        self.list_url = '/api/books/'
        self.create_url = '/api/books/create/'
        self.detail_url = f'/api/books/{self.book1.pk}/'
        self.update_url = f'/api/books/{self.book1.pk}/update/'
        self.delete_url = f'/api/books/{self.book1.pk}/delete/'

    # ---------- READ ----------
    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_single_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Django Unchained")

    # ---------- CREATE ----------
    def test_create_book_requires_auth(self):
        data = {"title": "New Book", "author": "Anon", "publication_year": 2024}
        # Unauthenticated -> 403
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated -> 201
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    # ---------- UPDATE ----------
    def test_update_book(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.put(self.update_url,
                                   {"title": "Updated", "author": "Tarantino", "publication_year": 2013})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated")

    # ---------- DELETE ----------
    def test_delete_book(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    # ---------- FILTERING ----------
    def test_filter_books_by_author(self):
        response = self.client.get(f'{self.list_url}?author=Guido')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ---------- SEARCH ----------
    def test_search_books(self):
        response = self.client.get(f'{self.list_url}?search=django')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Django Unchained")

    # ---------- ORDERING ----------
    def test_order_books_by_year_desc(self):
        response = self.client.get(f'{self.list_url}?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b['publication_year'] for b in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    # ---------- PERMISSIONS ----------
    def test_update_requires_auth(self):
        # Unauthenticated user trying to update
        response = self.client.put(self.update_url,
                                   {"title": "Hack", "author": "Anon", "publication_year": 2025})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
