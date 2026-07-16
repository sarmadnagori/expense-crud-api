from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)



def test_get_single_expense(expense):     # ← asks for the fixture
    resp = client.get(f"/expenses/{expense['id']}")
    assert resp.status_code == 200



def test_create_expense_returns_201():
    response = client.post("/expenses", json={"description": "coffee", "amount": 300})
    assert response.status_code == 201
    new_id = response.json()["id"]           # the id, now available
    client.delete(f"/expenses/{new_id}") 

def test_delete_missing_expense_returns_404():
    response = client.delete("/expenses/999999")
    assert response.status_code == 404


def test_update_missing_expense_returns_404():
    response = client.put("/expenses/999999", json={"amount": 500})
    assert response.status_code == 404


@pytest.fixture                                   # NEW: the fixture
def expense():
    response = client.post("/expenses", json={"description": "test coffee", "amount": 450})
    data = response.json()
    yield data                                    # hand it to the test
    client.delete(f"/expenses/{data['id']}")      # cleanup after test finishes

def test_delete_then_get_returns_404(expense):
    assert client.delete(f"/expenses/{expense['id']}").status_code == 204
    assert client.get(f"/expenses/{expense['id']}").status_code == 404

def test_rejects_empty_description():
    response = client.post("/expenses", json={"description": "", "amount": 500})
    assert response.status_code == 422


def test_rejects_negative_amount():
    response = client.post("/expenses", json={"description": "coffee", "amount": -500})
    assert response.status_code == 422