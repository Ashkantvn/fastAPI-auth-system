import pytest
from database import Session, Base, engine
from main import app


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    test_session = Session()
    try:
        yield test_session
    finally:
        Base.metadata.drop_all(bind=engine)
        test_session.close()


