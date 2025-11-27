import pytest
from database import Session, Base, get_db, engine
from main import app

Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    test_session = Session()
    try:
        yield test_session
    finally:
        test_session.close()

def override_get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


