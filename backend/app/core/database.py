"""Database setup."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _build_engine():
    if settings.database_url.startswith("sqlite"):
        return create_engine(
            settings.database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    return create_engine(settings.database_url, pool_pre_ping=True)


engine = _build_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

_is_initialized = False


def init_database() -> None:
    global _is_initialized
    if _is_initialized:
        return
    from app.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _is_initialized = True


def get_db_session() -> Generator[Session, None, None]:
    init_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def reset_database_for_tests() -> None:
    global _is_initialized
    from app.db import models  # noqa: F401

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    _is_initialized = True
