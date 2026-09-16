import os

import pytest

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite://")


@pytest.fixture(autouse=True)
def clean_database() -> None:
    from app.core.database import reset_database_for_tests
    from app.domain.recommendations.repository import clear_all_recommendations_for_tests

    reset_database_for_tests()
    clear_all_recommendations_for_tests()
