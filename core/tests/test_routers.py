from fastapi.testclient import TestClient
from main import app

class TestRouters:
    def setup_method(self):
        self.client = TestClient(app)

    def test_profilte_route(self):
        # Only let authenticated users access the profile route
        response = self.client.get("/profile")
        assert response.status_code == 401 
        assert response.json() == {"detail": "Not authenticated"}
