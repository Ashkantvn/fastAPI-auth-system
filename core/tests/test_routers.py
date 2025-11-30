from fastapi.testclient import TestClient
from models.db.user_model import User
from main import app

class TestRouters:
    def setup_method(self):
        self.client = TestClient(app)

    def test_profile_route_200(self, user):
        response = self.client.get(f"api/v1/users/profile/{user.username}")
        assert response.status_code == 200
        assert "profile" in response.json()

    def test_profile_route_404(self):
        response = self.client.get("api/v1/users/profile/nonexistent")
        assert response.status_code == 404
        assert response.json()["detail"] == "Profile not found"

    def test_login_route_200(self, user):
        response = self.client.post(
            "api/v1/users/login",
            data={"username": user.username, "password": "testpassword"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_route_400(self):
        response = self.client.post(
            "api/v1/users/login",
            data={"username": "wronguser", "password": "wrongpassword"}
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Incorrect username or password"

    def test_signup_route_201(self, db_session):
        response = self.client.post(
            "api/v1/users/signup",
            json={"username": "newuser", "password": "newpassword"}
        )
        assert response.status_code == 201
        assert response.json()["data"] == "User created successfully"
        assert "access_token" in response.json()
        # Test user is created
        profile_exist = db_session.query(User).filter_by(username="newuser").first()
        assert profile_exist is not None

    def test_signup_route_400(self, user):
        response = self.client.post(
            "api/v1/users/signup",
            json={"username": user.username, "password": "testpassword"}
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already registered"

    def test_logout_route_204(self, auth_client):
        response = auth_client.post("api/v1/users/logout")
        assert response.status_code == 204

    def test_logout_route_401(self):
        response = self.client.post("api/v1/users/logout")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_delete_user_route_204(self, user, db_session, auth_client):
        response = auth_client.delete(f"api/v1/users/delete")
        assert response.status_code == 204
        # Verify user is deleted
        profile_exist = db_session.query(User).filter_by(username=user.username).first()
        assert profile_exist is None

    def test_delete_user_route_401(self):
        response = self.client.delete("api/v1/users/delete")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"