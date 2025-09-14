from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Book

def search_books(request):
    query = request.GET.get('q', '')
    # Safe ORM filtering prevents SQL injection
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': query})
