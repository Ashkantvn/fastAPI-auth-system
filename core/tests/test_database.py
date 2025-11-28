from sqlalchemy import text
from database import engine

class TestDatabase:
    def test_connection(self, db_session):
        result = db_session.execute(text("SELECT 1")).scalar()
        assert result == 1

    def test_user_table_exists(self):
        inspector = engine.inspect(engine)
        tables = inspector.get_table_names()
        assert "user" in tables