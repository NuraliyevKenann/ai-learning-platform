# Backend

FastAPI backend for the adaptive learning platform.

This starts as a modular monolith. The application is one deployable backend,
but the code is split by responsibility:

- `api/` exposes HTTP endpoints.
- `domain/` contains product concepts and business services.
- `learning_engine/` contains deterministic mastery and recommendation logic.
- `ai/` contains optional LLM integration boundaries.
- `core/` contains application configuration and infrastructure helpers.

Important boundary:

```text
API endpoint -> service -> repository/database
                 |
                 -> learning_engine
                 -> ai client, later
```
