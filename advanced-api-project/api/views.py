# api/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # read-only for unauthenticated users

    """
    GET /api/books/
    Supports:
      - Filtering: ?title=...&author=...&publication_year=...
      - Searching: ?search=keyword
      - Ordering: ?ordering=title  or ?ordering=-publication_year
    """
    # Advanced query capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    #  Filtering
    filterset_fields = ['title', 'author', 'publication_year']

    #  Searching
    search_fields = ['title', 'author']

    #  Ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default order

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # must be logged in

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

