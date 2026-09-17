"""SQLAlchemy persistence models."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserRecord(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class SessionRecord(Base):
    __tablename__ = "sessions"

    token: Mapped[str] = mapped_column(String(160), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class KnowledgeStateRecord(Base):
    __tablename__ = "knowledge_states"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    skill_id: Mapped[str] = mapped_column(String(120), primary_key=True)
    mastery: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)


class UserCourseSelectionRecord(Base):
    __tablename__ = "user_course_selections"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    course_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    selected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class GoalRecord(Base):
    __tablename__ = "goals"

    id: Mapped[str] = mapped_column(String(120), primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class TopicRecord(Base):
    __tablename__ = "topics"

    id: Mapped[str] = mapped_column(String(120), primary_key=True)
    goal_id: Mapped[str] = mapped_column(ForeignKey("goals.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    skill_id: Mapped[str] = mapped_column(String(120), nullable=False)
    order: Mapped[int] = mapped_column(nullable=False)


class ExerciseRecord(Base):
    __tablename__ = "exercises"

    id: Mapped[str] = mapped_column(String(120), primary_key=True)
    topic_id: Mapped[str] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), index=True)
    skill_id: Mapped[str] = mapped_column(String(120), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    expected_answer: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(40), nullable=False)
    order: Mapped[int] = mapped_column(nullable=False)


class AttemptRecord(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    exercise_id: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    old_mastery: Mapped[float] = mapped_column(Float, nullable=False)
    new_mastery: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CurrentRecommendationRecord(Base):
    __tablename__ = "current_recommendations"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    type: Mapped[str] = mapped_column(String(80), nullable=False)
    exercise_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
