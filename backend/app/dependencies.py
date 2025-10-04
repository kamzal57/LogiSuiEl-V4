from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .core.config import get_settings
from .core.security import assert_token_subject, decode_token
from .database import get_db
from .models import Role, User

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: str = Security(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    payload = decode_token(token, settings.tokens.secret_key, settings.tokens.algorithm)
    username = assert_token_subject(payload)

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur introuvable")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Compte inactif")
    await db.refresh(user, attribute_names=["preferences"])
    return user


def require_role(*roles: Role):
    async def _checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
        return current_user

    return _checker


async def get_current_active_teacher(
    current_user: User = Depends(require_role(Role.ADMIN, Role.TEACHER)),
) -> User:
    return current_user


async def get_current_admin(
    current_user: User = Depends(require_role(Role.ADMIN)),
) -> User:
    return current_user


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db():
        yield session
