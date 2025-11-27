import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.mark.fastapi
class TestRouters:
    def setup_method(self):
        self.client = TestClient(app)
        