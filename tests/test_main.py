from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == \
        "Employee Leave Management API is running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_leaves():
    response = client.get("/api/leaves")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_leave():
    response = client.post(
        "/api/leaves",
        json={
            "employee_name": "Sharan",
            "leave_type": "Sick Leave",
            "start_date": "2026-08-10",
            "end_date": "2026-08-11",
            "reason": "Medical rest",
        },
    )

    assert response.status_code == 201
    assert response.json()["employee_name"] == "Sharan"
    assert response.json()["status"] == "Pending"


def test_invalid_dates():
    response = client.post(
        "/api/leaves",
        json={
            "employee_name": "Sharan",
            "leave_type": "Casual Leave",
            "start_date": "2026-08-15",
            "end_date": "2026-08-12",
            "reason": "Personal work",
        },
    )

    assert response.status_code == 400
