# Advanced API Project – Generic Views

- **BookListCreateView**: List all books or create new ones (POST requires authentication).
- **BookDetailView**: Retrieve, update, or delete a single book (update/delete require authentication).

Permissions:  
- Unauthenticated users → Read-only.
- Authenticated users → Full CRUD.

### Advanced Query Features

**Filtering**  
Use query params:  
`GET /api/books/?author=Rowling&publication_year=2007`

**Search**  
Text search on title/author:  
`GET /api/books/?search=philosopher`

**Ordering**  
Sort results:  
`GET /api/books/?ordering=title` or  
`GET /api/books/?ordering=-publication_year` (descending)
