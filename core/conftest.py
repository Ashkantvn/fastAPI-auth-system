import pytest
from database import Session, Base, engine
from main import app
from models.db.user_model import User
from fastapi.testclient import TestClient

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
    resp = client.post(
        "/api/v1/users/token",
        data={"username": user.username, "password": "testpassword"}
    )
    if resp.status_code != 200:
        # bubble up useful info for debugging tests
        raise RuntimeError(f"Failed to obtain token in auth_client fixture: {resp.status_code} {resp.text}")
    token = resp.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client
    client.close()