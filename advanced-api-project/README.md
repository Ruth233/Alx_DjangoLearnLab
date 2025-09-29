### Advanced API Project – Custom DRF Generic Views
- **BookListView**: GET /api/books/ — public.
- **BookDetailView**: GET /api/books/<id>/ — public.
- **BookCreateView**: POST /api/books/create/ — authenticated.
- **BookUpdateView**: PUT/PATCH /api/books/<id>/update/ — authenticated.
- **BookDeleteView**: DELETE /api/books/<id>/delete/ — authenticated.

**Permissions**: Read is open; write requires login.  
**Custom Behavior**: `perform_create` allows extra validation or attaching user data.
