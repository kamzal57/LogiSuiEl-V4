from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import get_settings
from ..core.security import create_token, get_password_hash, verify_password
from ..database import get_db
from ..dependencies import get_current_user
from ..models import Role, User
from ..core.security import decode_token
from ..schemas import RefreshRequest, Token, TokenPayload, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Compte inactif")

    access_token_expires = timedelta(minutes=settings.tokens.access_token_expire_minutes)
    refresh_token_expires = timedelta(minutes=settings.tokens.refresh_token_expire_minutes)

    access_token = create_token(
        {"sub": user.username, "role": user.role.value, "type": "access"},
        settings.tokens.secret_key,
        settings.tokens.algorithm,
        access_token_expires,
    )
    refresh_token = create_token(
        {"sub": user.username, "role": user.role.value, "type": "refresh"},
        settings.tokens.secret_key,
        settings.tokens.algorithm,
        refresh_token_expires,
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=int(access_token_expires.total_seconds()),
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(request: RefreshRequest, db: AsyncSession = Depends(get_db)) -> Token:
    payload: TokenPayload = decode_token(
        request.refresh_token,
        settings.tokens.secret_key,
        settings.tokens.algorithm,
    )
    if payload.sub is None or payload.role is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token non valide")
    if payload.type != "refresh":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token non valide")

    result = await db.execute(select(User).where(User.username == payload.sub))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")

    access_token_expires = timedelta(minutes=settings.tokens.access_token_expire_minutes)
    refresh_token_expires = timedelta(minutes=settings.tokens.refresh_token_expire_minutes)

    access_token = create_token(
        {"sub": user.username, "role": user.role.value, "type": "access"},
        settings.tokens.secret_key,
        settings.tokens.algorithm,
        access_token_expires,
    )
    refresh_token = create_token(
        {"sub": user.username, "role": user.role.value, "type": "refresh"},
        settings.tokens.secret_key,
        settings.tokens.algorithm,
        refresh_token_expires,
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=int(access_token_expires.total_seconds()),
    )


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user, from_attributes=True)


async def ensure_default_users(db: AsyncSession) -> None:
    """Create default admin and teacher if missing."""

    async def _get_user(username: str) -> User | None:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    for username, password, role in [
        (settings.admin_default_username, settings.admin_default_password, Role.ADMIN),
        (settings.teacher_default_username, settings.teacher_default_password, Role.TEACHER),
    ]:
        user = await _get_user(username)
        if not user:
            new_user = User(
                username=username,
                hashed_password=get_password_hash(password),
                role=role,
                full_name=username.capitalize(),
            )
            db.add(new_user)
    await db.commit()
