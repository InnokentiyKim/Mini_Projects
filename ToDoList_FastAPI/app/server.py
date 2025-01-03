from fastapi import FastAPI, HTTPException
from sqlalchemy import func, select
from lifespan import lifespan
from models import Todo, User, Token
from dependency import SessionDependency, TokenDependency
from schema import (GetTodoResponse, CreateTodoResponse, CreateTodoRequest,
                    UpdateTodoResponse, UpdateTodoRequest, DeleteTodoResponse,
                    CreateUserRequest, CreateUserResponse,
                    LoginRequest, LoginResponse)
import crud
import auth
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
async def create_todo(todo_request: CreateTodoRequest, session: SessionDependency, token: TokenDependency):
    todo = Todo(
        title=todo_request.title,
        description=todo_request.description,
        important=todo_request.important,
        user_id=token.user_id
    )
    await crud.add_item(session, todo)
    return todo.id_dict


@app.patch("/api/v1/todo/{todo_id}", response_model=UpdateTodoResponse, tags=["todo"])
async def update_todo(todo_id: int, todo_request: UpdateTodoRequest,
                      session: SessionDependency, token: TokenDependency):
    todo_json = todo_request.model_dump(exclude_unset=True)
    if todo_request.done:
        todo_json['end_time'] = func.now()
    todo = await crud.get_item_by_id(session, Todo, todo_id)
    if todo.user_id != token.user_id and token.user.role != 'admin':
        raise HTTPException(403, "Access denied")
    for field, value in todo_json.items():
        setattr(todo, field, value)
    await crud.add_item(session, todo)
    return todo.id_dict


@app.delete("/api/v1/todo/{todo_id}", response_model=DeleteTodoResponse, tags=["todo"])
async def delete_todo(todo_id: int, session: SessionDependency):
    todo = await crud.get_item_by_id(session, Todo, todo_id)
    await crud.delete_item(session, todo)
    return STATUS_DELETED


@app.post("/api/v1/user", response_model=CreateUserResponse, tags=["user"])
async def create_user(session: SessionDependency, user_request: CreateUserRequest):
    user_request_dict = user_request.model_dump()
    user_request_dict["password"] = auth.hash_password(user_request_dict["password"])
    user = User(**user_request_dict)
    await crud.add_item(session, user)
    return user.id_dict


@app.post("/api/v1/login", response_model=LoginResponse, tags=['user'])
async def login(login_request: LoginRequest, session: SessionDependency):
    user_query = select(User).where(User.name == login_request.name)
    user = await session.scalar(user_query)
    if user is None:
        raise HTTPException(status_code=401, detail="Username or password is incorrect")
    if not auth.check_password(login_request.password, user.password):
        raise HTTPException(status_code=401, detail="Username or password is incorrect")
    token = Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict

