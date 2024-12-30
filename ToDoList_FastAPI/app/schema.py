import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Literal


class IdResponseBase(BaseModel):
    id : int

class GetTodoResponse(BaseModel):
    id: int
    title: str
    description: str
    important: bool
    done: bool
    start_time: datetime
    end_time: datetime | None


class CreateTodoRequest(BaseModel):
    title: str
    description: str
    important: bool


class CreateTodoResponse(IdResponseBase):
    pass


class UpdateTodoRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    important: bool | None = None
    done: bool | None = None


class UpdateTodoResponse(IdResponseBase):
    pass


class StatusResponse(BaseModel):
    status: Literal['deleted']


class DeleteTodoResponse(StatusResponse):
    pass


class BaseUserRequest(BaseModel):
    name: str
    password: str


class CreateUserRequest(BaseUserRequest):
    pass


class CreateUserResponse(IdResponseBase):
    pass


class LoginRequest(BaseUserRequest):
    pass


class LoginResponse(BaseModel):
    token: uuid.UUID


