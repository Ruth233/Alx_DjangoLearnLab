# Advanced API Project – Generic Views

- **BookListCreateView**: List all books or create new ones (POST requires authentication).
- **BookDetailView**: Retrieve, update, or delete a single book (update/delete require authentication).

Permissions:  
- Unauthenticated users → Read-only.
- Authenticated users → Full CRUD.
