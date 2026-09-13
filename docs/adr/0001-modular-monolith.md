# ADR 0001: Use A Modular Monolith

## Status

Accepted

## Context

The project is built by a small student team. The team needs to understand the
system while building it. Microservices would add deployment, networking,
observability, and data consistency complexity before the product needs it.

## Decision

Start with a modular monolith: one backend application with clear internal
module boundaries.

## Consequences

- Easier to run locally.
- Easier to debug.
- Easier to refactor while learning.
- Requires discipline to keep modules clean.
