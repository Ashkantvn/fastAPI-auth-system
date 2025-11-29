from fastapi.testclient import TestClient
from main import app

class TestRouters:
    def setup_method(self):
        self.client = TestClient(app)

    def test_profile_route_200(self, user):
        response = self.client.get(f"/profile/{user.username}")
        assert response.status_code == 200
        assert "profile" in response.json()

    def test_profile_route_404(self):
        response = self.client.get("/profile/nonexistent")
        assert response.status_code == 404
        assert response.json()["detail"] == "Profile not found"
