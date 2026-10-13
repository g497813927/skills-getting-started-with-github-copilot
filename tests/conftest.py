import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    """Provide a clean FastAPI client for each test."""
    original_activities = copy.deepcopy(activities)

    try:
        with TestClient(app) as test_client:
            activities.clear()
            activities.update(copy.deepcopy(original_activities))
            yield test_client
    finally:
        activities.clear()
        activities.update(copy.deepcopy(original_activities))
