from django.shortcuts import render

# Create your views here.
<<<<<<< HEAD
from django.shortcuts import render
from .models import Book

def search_books(request):
    query = request.GET.get('q', '')
    # Safe ORM filtering prevents SQL injection
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': query})
=======
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book

# Anyone with can_view can see the list
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    # logic to create a book
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    # logic to edit a book
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    # logic to delete a book
    pass
>>>>>>> 2ab008403daefe1cb6e27ad3abac24c4a6c51790
