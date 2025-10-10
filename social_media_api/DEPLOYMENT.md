# Deployment Guide — Social Media API

**Live App:** [https://social-media-api.onrender.com](https://alx-djangolearnlab-3n7a.onrender.com)

## Steps Followed
1. Configured Django for production (DEBUG=False, ALLOWED_HOSTS, security).
2. Installed gunicorn, whitenoise, dj-database-url, psycopg2-binary.
3. Created `Procfile` and `requirements.txt`.
4. Pushed to GitHub.
5. Deployed to Render.
6. Configured environment variables and ran migrations.

## Notes
- Static files served with WhiteNoise.
- Database: PostgreSQL (Render-hosted).
- Server: Gunicorn + Render reverse proxy.
