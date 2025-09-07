from relationship_app.models import Author, Book, Library, Librarian
from relationship_app.query_samples import get_books_by_author, get_books_in_library, get_librarian_for_library

# Create sample data
a1 = Author.objects.create(name="George Orwell")
b1 = Book.objects.create(title="1984", author=a1)
b2 = Book.objects.create(title="Animal Farm", author=a1)

lib = Library.objects.create(name="Central Library")
lib.books.add(b1, b2)

librarian = Librarian.objects.create(name="Alice", library=lib)

# Run queries
print(get_books_by_author("George Orwell"))   # <QuerySet [<Book: 1984>, <Book: Animal Farm>]>
print(get_books_in_library("Central Library"))  # <QuerySet [<Book: 1984>, <Book: Animal Farm>]>
print(get_librarian_for_library("Central Library"))  # Alice
