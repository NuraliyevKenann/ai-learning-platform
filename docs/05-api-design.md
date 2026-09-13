# API Design

## Principles

- Use versioned routes under `/api/v1`.
- Keep endpoints thin.
- Put business logic in services.
- Return frontend-friendly response shapes.
- Use consistent error responses.

## Initial Endpoints

```text
GET  /api/v1/health
GET  /api/v1/goals
GET  /api/v1/topics
GET  /api/v1/exercises
POST /api/v1/attempts
GET  /api/v1/knowledge/state
GET  /api/v1/recommendations/current
```
