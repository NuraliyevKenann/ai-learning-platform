# ADR 0002: Use FastAPI, React, And PostgreSQL

## Status

Accepted

## Context

The MVP needs a backend API, a browser UI, and relational data storage for users,
content, attempts, evaluations, and knowledge states.

## Decision

Use:

- FastAPI for the backend API;
- React for the frontend;
- PostgreSQL for the database.

## Consequences

- The stack is practical and common.
- The team learns real API and database development.
- PostgreSQL adds setup cost, handled with Docker Compose.
