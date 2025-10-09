# Social Media API (accounts)

## Setup
1. Install deps: `pip install django djangorestframework djangorestframework-authtoken`
2. Migrate: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Run server: `python manage.py runserver`

## Endpoints
- `POST /api/accounts/register/` — register; returns profile + token
- `POST /api/accounts/login/` — login; returns token
- `GET/PUT /api/accounts/profile/` — view/update authenticated user profile (Token auth required)

## Auth
Use `Authorization: Token <token>` header on protected endpoints.

## Models
`CustomUser` extends `AbstractUser` with:
- `bio`, `profile_picture` (ImageField), `followers` (ManyToMany to CustomUser; symmetrical=False)

## Posts & Comments API

Base endpoint: `/api/`

### Posts
- GET `/api/posts/` — list posts (support `?search=`, `?ordering=created_at`, `?author__username=`)
- POST `/api/posts/` — create a post (auth required)
- GET `/api/posts/{id}/` — retrieve
- PUT/PATCH `/api/posts/{id}/` — update (author only)
- DELETE `/api/posts/{id}/` — delete (author only)
- GET `/api/posts/{id}/comments/` — list comments for post (paginated)

### Comments
- GET `/api/comments/` — list comments
- POST `/api/comments/` — create comment (include `post` id in body; auth required)
- GET/PUT/DELETE `/api/comments/{id}/` — manage a comment (author only)

### Pagination & Filtering
- Pagination: `?page=2` (default page size from settings)
- Searching posts: `?search=keyword`
- Filtering by author: `?author__username=username`
