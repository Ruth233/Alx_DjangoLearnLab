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
