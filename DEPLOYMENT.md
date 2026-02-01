# Deployment (Easy / Real-world)

## The easiest way (Docker Compose)

Prereqs:
- Docker + Docker Compose

Run:
```bash
docker compose up --build
```

Then open:
- Landing page: http://localhost:3000
- API docs (Swagger): http://localhost:8000/docs
- Health: http://localhost:8000/health

## Environment variables

Backend:
- `APP_ENV`: `dev` or `prod`
- `CORS_ALLOW_ORIGINS`: comma-separated list (example: `http://localhost:3000,https://your-domain.com`)

Frontend:
- `NEXT_PUBLIC_API_BASE_URL`: used to link to your API docs/health from the landing page.

## Production notes

- Put the API behind a reverse proxy (Nginx/Caddy) and enable HTTPS.
- Add auth + rate limiting in front of `/predict` and `/batch-predict`.
- Tighten CORS to only the domains you control.
