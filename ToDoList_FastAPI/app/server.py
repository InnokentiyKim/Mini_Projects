from fastapi import FastAPI
from sqlalchemy import func
from lifespan import lifespan
from models import Todo
from dependency import SessionDependency
from schema import (GetTodoResponse, CreateTodoResponse, CreateTodoRequest,
                    UpdateTodoResponse, UpdateTodoRequest, DeleteTodoResponse)
import crud
from constants import STATUS_DELETED


app = FastAPI(
    title="Hello world",
    terms_of_service="",
    description="awesome project",
    lifespan=lifespan,
)


@app.get("/api/v1/todo/{todo_id}", response_model=GetTodoResponse, tags=["todo"])
async def get_todo(session: SessionDependency, todo_id: int):
    todo_item = await crud.get_item_by_id(session, Todo, todo_id)
    return todo_item.dict


@app.post("/api/v1/todo", response_model=CreateTodoResponse, tags=["todo"])
async def create_todo(todo_request: CreateTodoRequest, session: SessionDependency):
    todo = Todo(title=todo_request.title, description=todo_request.description, important=todo_request.important)
    await crud.add_item(session, todo)
    return todo.id_dict


@app.patch("/api/v1/todo/{todo_id}", response_model=UpdateTodoResponse, tags=["todo"])
async def update_todo(todo_id: int, todo_request: UpdateTodoRequest, session: SessionDependency):
    todo_json = todo_request.dict(exclude_unset=True)
    if todo_request.done:
        todo_json['end_time'] = func.now()
    todo = await crud.get_item_by_id(session, Todo, todo_id)
    for field, value in todo_json.items():
        setattr(todo, field, value)
    await crud.add_item(session, todo)
    return todo.id_dict


@app.delete("/api/v1/todo/{todo_id}", response_model=DeleteTodoResponse, tags=["todo"])
async def delete_todo(todo_id: int, session: SessionDependency):
    todo = await crud.get_item_by_id(session, Todo, todo_id)
    await crud.delete_item(session, todo)
    return STATUS_DELETED
