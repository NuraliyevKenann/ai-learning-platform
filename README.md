# AI Learning Platform

Adaptive learning platform foundation for learning product development, backend,
frontend, databases, AI integration, and future ML.

The project starts as a modular monolith:

- `backend/` contains the FastAPI application, domain modules, and learning engine.
- `frontend/` contains the React application structure.
- `docs/` contains product, architecture, and decision documents.

Core principle:

```text
LLM suggests and explains.
Learning engine decides.
Database stores truth.
```

## Current Stage

Foundation only. The first implementation target is the smallest complete
learning loop:

```text
Choose goal
-> see roadmap
-> solve exercise
-> submit attempt
-> receive evaluation
-> update knowledge state
-> get next recommendation
```

## Planned Stack

- Backend: FastAPI
- Frontend: React + Vite
- Database: PostgreSQL
- ORM/Migrations: SQLAlchemy + Alembic
- Architecture: modular monolith
- AI: separate integration layer, added after the deterministic loop works
- ML: future stage, after enough learning data exists
