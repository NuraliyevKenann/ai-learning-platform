# System Architecture

## Style

Modular monolith.

The system starts as one backend application and one frontend application. The
backend is internally split into modules so future features can be added without
turning route handlers into business-logic containers.

## Backend Boundary

```text
API endpoint
-> domain service
-> repository/database
-> learning_engine when a learning decision is needed
-> ai client later when language generation is needed
```

## First Runtime Components

```text
React frontend
FastAPI backend
PostgreSQL database
```

## Later Components

- Background worker for slow AI/project analysis jobs.
- Redis for queues or caching if needed.
- ML training pipeline after enough attempt data exists.
- Vector search only if trusted content search becomes necessary.
