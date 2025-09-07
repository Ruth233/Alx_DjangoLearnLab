from relationship_app.models import Author, Book, Library, Librarian

# Query 1: All books by a specific author
def get_books_by_author(author_name):
    return Book.objects.filter(author__name=author_name)


# Query 2: All books in a specific library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()


# Query 3: The librarian for a library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian
