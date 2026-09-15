"""Compatibility facade for the in-memory MVP repositories and services."""

from app.domain.assessment.service import submit_attempt
from app.domain.content.repository import list_exercises, list_goals, list_topics
from app.domain.learning.service import get_knowledge_state
from app.domain.recommendations.repository import get_current_recommendation
