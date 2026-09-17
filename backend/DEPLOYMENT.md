# Backend deployment notes

Use these settings when the backend runs online instead of on your computer.

## Required environment variables

```env
APP_ENV=production
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
CORS_ORIGINS=https://your-frontend-domain.com
SESSION_COOKIE_SAMESITE=none
SESSION_COOKIE_NAME=skillway_session
SESSION_MAX_AGE_SECONDS=604800
```

`CORS_ORIGINS` must be the exact frontend URL. If the frontend URL changes, update this value.

`SESSION_COOKIE_SAMESITE=none` is needed when frontend and backend are on different domains. Production cookies are secure automatically when `APP_ENV=production`, so the backend must run through HTTPS.

## Start command

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Database migration

Run migrations before serving traffic:

```bash
python -m alembic upgrade head
```

## Health check

```text
GET /api/v1/health
```
