### Advanced API Project – Custom DRF Generic Views
- **BookListView**: GET /api/books/ — public.
- **BookDetailView**: GET /api/books/<id>/ — public.
- **BookCreateView**: POST /api/books/create/ — authenticated.
- **BookUpdateView**: PUT/PATCH /api/books/<id>/update/ — authenticated.
- **BookDeleteView**: DELETE /api/books/<id>/delete/ — authenticated.

**Permissions**: Read is open; write requires login.  
**Custom Behavior**: `perform_create` allows extra validation or attaching user data.
### Advanced Query Parameters
**Endpoint:** `GET /api/books/`

- **Filtering**
  - By title: `?title=The Hobbit`
  - By author: `?author=Tolkien`
  - By year: `?publication_year=1937`
  - 
- **Searching**
  - Text search across `title` and `author`: `?search=tolkien`

- **Ordering**
  - Ascending: `?ordering=title`
  - Descending: `?ordering=-publication_year`

## Running Tests
Unit tests live in `api/test_views.py` and cover:
- CRUD operations for the Book API.
- Filtering (?author=...), searching (?search=...), and ordering (?ordering=...).
- Permission enforcement for create/update/delete.

Run tests:
```bash
python manage.py test api
