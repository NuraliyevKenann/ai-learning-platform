"""User domain model."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    id: str
    email: str
    display_name: str
    password_hash: str
    created_at: datetime
