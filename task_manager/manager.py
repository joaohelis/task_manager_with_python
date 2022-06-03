from enum import Enum
from lib2to3.pytree import Base
from pydoc import describe
from uuid import UUID, uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, constr


class StatusEnum(str, Enum):
    finished = "finished"
    not_finished = "not finished"


class TaskEntry(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(max_length=140)
    status: StatusEnum = StatusEnum.not_finished


class Task(TaskEntry):
    id: UUID


app = FastAPI()

TASKS = [
    {
        "id": "1",
        "title": "fazer compras",
        "description": "comprar leite e ovos",
        "status": "não finalizado",
    },
    {
        "id": "2",
        "title": "levar o cachorro para tosar",
        "description": "está muito peludo",
        "status": "não finalizado",
    },
    {
        "id": "3",
        "title": "lavar roupas",
        "description": "estão sujas",
        "status": "não finalizado",
    },
]


@app.get("/tasks")
def list():
    return TASKS


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create(task: TaskEntry):
    new_task = task.dict()
    new_task.update({"id": uuid4()})
    TASKS.append(new_task)
    return new_task
