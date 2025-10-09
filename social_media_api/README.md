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
