import uuid

from config import DSN
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy import String, Integer, Boolean, DateTime, UUID, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


engine = create_async_engine(DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


class User(Base):
    __tablename__ = 'todo_user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    tokens: Mapped[list["Token"]] = relationship("Token", lazy="joined", back_populates='user')
    todos: Mapped[list["Todo"]] = relationship("Todo", lazy="joined", back_populates='user')


class Token(Base):
    __tablename__ = "token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, server_default=func.gen_random_uuid())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("todo_user.id"))
    user: Mapped["User"] = relationship("User", lazy="joined", back_populates='tokens')

    @property
    def dict(self):
        return {"token": self.token}


class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    important: Mapped[bool] = mapped_column(Boolean, default=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("todo_user.id"))
    user: Mapped["User"] = relationship("User", lazy="joined", back_populates='todos')

    @property
    def dict(self):
        end_time = None
        if self.end_time is not None:
            end_time = self.end_time.isoformat()
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "important": self.important,
            "done": self.done,
            "start_time": self.start_time.isoformat(),
            "end_time": end_time,
        }

ORM_OBJ = Todo | User | Token
ORM_CLS = type[Todo] | type[User] | type[Token]

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
