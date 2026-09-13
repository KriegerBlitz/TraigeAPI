from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_patient():
    response = client.post(
        "/patients",
        json={"name": "Jane Doe", "age": 70, "pain_level": 8, "notes": "Chest discomfort"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Jane Doe"
    # Age > 65 gives +20, pain 8 gives 80 -> max capped at 100
    assert data["urgency_score"] == 100

def test_get_patients():
    response = client.get("/patients")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
