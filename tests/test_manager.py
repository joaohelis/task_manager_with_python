from http import client
from urllib import response

from fastapi import status
from fastapi.testclient import TestClient

from task_manager.manager import TASKS, app


def test_when_listing_tasks_the_return_status_should_be_200():
    client = TestClient(app)
    response = client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK


def test_when_listing_tasks_the_return_format_should_be_json():
    client = TestClient(app)
    response = client.get("/tasks")
    assert response.headers["Content-Type"] == "application/json"


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


def test_tasks_resource_should_accept_http_post():
    client = TestClient(app)
    response = client.post("/tasks")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


def test_task_creation_must_have_title():
    client = TestClient(app)
    response = client.post("/tasks", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_task_creation_must_contain_between_3_and_50_characters():
    client = TestClient(app)
    response = client.post("/tasks", json={"title": 2 * "*"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response = client.post("/tasks", json={"title": 51 * "*"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_task_creation_must_have_a_description():
    client = TestClient(app)
    response = client.post("/tasks", json={"title": "title"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_task_creation_must_have_a_description_with_max_lenght_of_140_characters():
    client = TestClient(app)
    response = client.post(
        "/tasks", json={"title": "title", "description": "*" * 141}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_when_creating_a_test_it_must_be_returned_as_response():
    client = TestClient(app)
    task = {"title": "title", "description": "description"}
    response = client.post("/tasks", json=task)
    created_task = response.json()
    print(created_task)
    assert task["title"] == created_task["title"]
    assert task["description"] == created_task["description"]
    TASKS.clear()


def test_when_creating_a_task_it_must_have_a_unique_identifier():
    client = TestClient(app)
    task_1 = {"title": "title 1", "description": "description 1"}
    task_2 = {"title": "title 2", "description": "description 2"}
    response_1 = client.post("/tasks", json=task_1)
    response_2 = client.post("/tasks", json=task_2)
    assert response_1.json()["id"] != response_2.json()["id"]
    TASKS.clear()


def test_task_must_have_a_state_with_not_finished_value_as_default():
    client = TestClient(app)
    task = {"title": "title", "description": "description"}
    response = client.post("/tasks", json=task)
    assert response.json()["status"] == "not finished"
    TASKS.clear()


def test_when_creating_a_task_the_status_code_must_be_201():
    client = TestClient(app)
    task = {"title": "title", "description": "description"}
    response = client.post("/tasks", json=task)
    assert response.status_code == status.HTTP_201_CREATED
    TASKS.clear()


def test_when_creating_a_task_it_must_be_persisted():
    client = TestClient(app)
    task = {"title": "title", "description": "description"}
    response = client.post("/tasks", json=task)
    assert len(TASKS) == 1
    TASKS.clear()
