from sqlalchemy import select

from ..core.config import get_settings
from ..database import SessionLocal
from ..models import AppConfig, Role, User, UserPreference
from ..core.security import get_password_hash

settings = get_settings()


async def bootstrap_defaults() -> None:
    async with SessionLocal() as session:
        if not await _has_users(session):
            await _create_default_users(session)
        await _ensure_config(session)
        await session.commit()


async def _has_users(session) -> bool:
    result = await session.execute(select(User.id).limit(1))
    return result.scalar_one_or_none() is not None


async def _create_default_users(session) -> None:
    admin = User(
        username=settings.admin_default_username,
        role=Role.ADMIN,
        hashed_password=get_password_hash(settings.admin_default_password),
        full_name="Administrateur",
    )
    teacher = User(
        username=settings.teacher_default_username,
        role=Role.TEACHER,
        hashed_password=get_password_hash(settings.teacher_default_password),
        full_name="Professeur Démo",
    )
    session.add_all([admin, teacher])
    await session.flush()

    session.add_all(
        [
            UserPreference(user=admin, locale="fr", available_widgets={"annuaire": True, "dictionnaire": True}),
            UserPreference(user=teacher, locale="fr", available_widgets={"annuaire": True}),
        ]
    )


async def _ensure_config(session) -> None:
    result = await session.execute(select(AppConfig).limit(1))
    config = result.scalar_one_or_none()
    if not config:
        config = AppConfig(
            school_name="Démo Collège",
            academic_year="2025-2026",
            periods={
                "trimestres": [
                    {"name": "Trimestre 1", "start": "2025-09-01", "end": "2025-12-15"},
                    {"name": "Trimestre 2", "start": "2026-01-05", "end": "2026-03-31"},
                    {"name": "Trimestre 3", "start": "2026-04-01", "end": "2026-07-06"},
                ]
            },
            timetable_settings={"week_mode": "AB", "hour_start": "08:00", "hour_end": "18:00"},
            appearance={"theme": "auto"},
            available_tools={
                "dashboard": True,
                "plan_de_classe": True,
                "evaluations": True,
                "vie_scolaire": True,
                "protocoles": True,
                "widgets": True,
            },
            class_mode_allowed_tools=["dashboard", "plan_de_classe", "widgets"],
            outside_class_allowed_tools=["evaluations", "vie_scolaire", "protocoles"],
            locale="fr",
        )
        session.add(config)
