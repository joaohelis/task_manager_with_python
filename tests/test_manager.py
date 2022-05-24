from fastapi.testclient import TestClient
from fastapi import status
from task_manager.manager import app, TASKS

def test_when_listing_tasks_the_return_status_should_be_200():
    client = TestClient(app)
    response = client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK

def test_when_listing_tasks_the_return_format_should_be_json():
    client = TestClient(app)
    response = client.get("/tasks")
    assert response.headers['Content-Type'] == "application/json"

def test_when_listing_tasks_the_return_should_be_a_list():
    client = TestClient(app)
    response = client.get("/tasks")
    assert isinstance(response.json(), list)


def test_when_listing_tasks_a_unique_task_should_have_an_id():
    TASKS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "title 1",
            "description": "description 1",
            "status": "finished",
        }
    )
    client = TestClient(app)
    response = client.get("/tasks")
    assert "id" in response.json().pop()
    TASKS.clear()

def test_when_listing_tasks_a_unique_task_should_have_a_description():
    TASKS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "title 1",
            "description": "description 1",
            "status": "finished",
        }
    )
    client = TestClient(app)
    response = client.get("/tasks")
    assert "description" in response.json().pop()
    TASKS.clear()

def test_when_listing_tasks_a_unique_task_should_have_a_status():
    TASKS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "title 1",
            "description": "description 1",
            "status": "finished",
        }
    )
    client = TestClient(app)
    response = client.get("/tasks")
    assert "status" in response.json().pop()
    TASKS.clear()
