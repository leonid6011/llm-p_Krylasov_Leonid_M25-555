from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.users import UserRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repo(
        session: AsyncSession = Depends(get_session)
        ) -> UserRepository:
    return UserRepository(session)

async def get_chat_repo(
        session: AsyncSession = Depends(get_session)
        ) -> ChatMessageRepository:
    return ChatMessageRepository(session)


async def get_auth_usecase(
        user_repo: UserRepository = Depends(get_user_repo)
        ) -> AuthUseCase:
    return AuthUseCase(user_repo)


async def get_chat_usecase(
        chat_repo: ChatMessageRepository = Depends(get_chat_repo)
        ) -> ChatUseCase:
    return ChatUseCase(chat_repo, OpenRouterClient())


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = decode_access_token(token)
        return int(payload["sub"])
    except (ValueError, KeyError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            ) from e
