import pytest
from database import Session, Base, engine
from main import app
from models.user_model import User

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    test_session = Session()
    try:
        yield test_session
    finally:
        Base.metadata.drop_all(bind=engine)
        test_session.close()

@pytest.fixture
def user(db_session):
    session = db_session
    user = User.create_user(
        session=session,
        username="testuser",
        password="testpassword"
    )
    try:
        yield user
    finally:
        session.delete(user)
        session.commit()
        session.close()