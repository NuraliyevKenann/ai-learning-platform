# Database Schema

This document will become the source of truth before SQLAlchemy models and
Alembic migrations are added.

## MVP Tables To Design

- users
- goals
- skills
- topics
- topic_skills
- learning_paths
- learning_path_steps
- content_items
- exercises
- exercise_skills
- attempts
- evaluations
- knowledge_states
- recommendations

## Design Rule

Do not store only lesson completion. Store evidence that updates skill mastery.
