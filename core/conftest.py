import pytest
from database import Session, Base, engine
from main import app
from models.db.user_model import User
from fastapi.testclient import TestClient
from utils.jwt_manager import create_access_token

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


@pytest.fixture
def auth_client(user):
    client = TestClient(app)
    token = create_access_token(user_id=user.id)
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client
    client.close()