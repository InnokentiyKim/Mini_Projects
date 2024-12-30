import uuid
import datetime
from models import Session, Token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from fastapi import Depends, Header, HTTPException
from config import TOKEN_TTL_SEC


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session, use_cache=True)]


async def get_token(x_token: Annotated[uuid.UUID, Header()], session: SessionDependency):
    token_query = select(Token).where(
        Token.token == x_token,
        Token.created_at >= datetime.datetime.now() - datetime.timedelta(seconds=TOKEN_TTL_SEC)
    )
    token = session.scalar(token_query)
    if token is None:
        raise HTTPException(401, "Invalid token")
    return token


TokenDependency = Annotated[Token, Depends(get_token)]
