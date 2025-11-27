from fastapi.testclient import TestClient
from main import app

class TestRouters:
    def setup_method(self):
        self.client = TestClient(app)