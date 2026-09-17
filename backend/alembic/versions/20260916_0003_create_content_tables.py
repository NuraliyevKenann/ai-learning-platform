"""create content tables

Revision ID: 20260916_0003
Revises: 20260916_0002
Create Date: 2026-09-16
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260916_0003"
down_revision: str | None = "20260916_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "goals",
        sa.Column("id", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "topics",
        sa.Column("id", sa.String(length=120), nullable=False),
        sa.Column("goal_id", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("skill_id", sa.String(length=120), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["goal_id"], ["goals.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_topics_goal_id"), "topics", ["goal_id"], unique=False)
    op.create_table(
        "exercises",
        sa.Column("id", sa.String(length=120), nullable=False),
        sa.Column("topic_id", sa.String(length=120), nullable=False),
        sa.Column("skill_id", sa.String(length=120), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("expected_answer", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.String(length=40), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_exercises_topic_id"), "exercises", ["topic_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_exercises_topic_id"), table_name="exercises")
    op.drop_table("exercises")
    op.drop_index(op.f("ix_topics_goal_id"), table_name="topics")
    op.drop_table("topics")
    op.drop_table("goals")
