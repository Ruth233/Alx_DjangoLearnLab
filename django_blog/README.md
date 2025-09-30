## Authentication Features
- **Register:** Users sign up with username, email, and password.
- **Login/Logout:** Managed via Django’s built-in auth views.
- **Profile:** Authenticated users can view and update email.

### Running
1. Ensure `blog` is in `INSTALLED_APPS`.
2. Run `python manage.py migrate` to apply auth tables.
3. Start the server: `python manage.py runserver`.
4. Visit `/register` to create an account.

CSRF protection is enabled via `{% csrf_token %}`.
Passwords are securely hashed using Django’s default PBKDF2.

## Blog Post Management

Routes:
- GET /posts/           -> list all posts
- GET /posts/new/       -> create (login required)
- GET /posts/<pk>/      -> detail
- GET /posts/<pk>/edit/ -> update (author only)
- GET /posts/<pk>/delete/ -> delete (author only)

Permissions:
- Anyone can view list/detail.
- Only authenticated users can create posts.
- Only the author (or staff) can edit/delete their posts.

To run:
- migrate, create superuser, runserver

## Comments

- Model: `Comment(post, author, content, created_at, updated_at)`
- Create: POST to `/post/<post_pk>/comments/new/` — requires login.
- Edit: GET/POST `/post/<post_pk>/comments/<comment_pk>/edit/` — only comment author.
- Delete: GET/POST `/post/<post_pk>/comments/<comment_pk>/delete/` — only comment author.

Inline commenting: the post detail page displays comments and an inline form for logged-in users.
To run tests:
    python manage.py test blog

## Tags & Search

- **Adding tags**: When creating or editing a post, enter comma-separated tags in the "tags" field (e.g. "django, python, tips"). New tags will be created automatically.
- **View posts by tag**: /tags/<tag_slug>/ (example: /tags/django/)
- **Search**: /search/?q=keyword — searches title, content, and tag names.

Notes:
- Tags appear on the post detail page. Click a tag to see posts that share it.
- For production or advanced features, consider using `django-taggit` or a full-text search backend.
