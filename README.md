# Catalog API

REST API for catalog categories and products built with FastAPI.

## Tech Stack

- FastAPI
- SQLAlchemy Async
- MySQL
- Docker
- Pydantic

## Run Project

```bash
docker compose up --build
```

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

phpMyAdmin:

```text
http://localhost:8080
```

## Environment Variables

Create `.env` file from `.env.example`.

```bash
cp .env.example .env
```