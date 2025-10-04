from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User, AppConfig, UserPreferences
from app.core.security import get_password_hash


async def create_default_users(db: AsyncSession):
    """Create default admin and teacher users."""
    # Check if users already exist
    result = await db.execute(select(User).where(User.username == "admin"))
    existing_admin = result.scalar_one_or_none()
    
    if not existing_admin:
        admin_user = User(
            username="admin",
            email="admin@logisuiel.local",
            hashed_password=get_password_hash("admin"),
            role="ADMIN",
            full_name="Administrator",
            is_active=True
        )
        db.add(admin_user)
        
        # Create preferences for admin
        admin_prefs = UserPreferences(
            user=admin_user,
            class_mode=False,
            language="fr",
            theme="light",
            widgets_enabled=["games", "directory", "dictionary", "favorites"]
        )
        db.add(admin_prefs)
    
    result = await db.execute(select(User).where(User.username == "test"))
    existing_teacher = result.scalar_one_or_none()
    
    if not existing_teacher:
        teacher_user = User(
            username="test",
            email="test@logisuiel.local",
            hashed_password=get_password_hash("test"),
            role="TEACHER",
            full_name="Test Teacher",
            is_active=True
        )
        db.add(teacher_user)
        
        # Create preferences for teacher
        teacher_prefs = UserPreferences(
            user=teacher_user,
            class_mode=False,
            language="fr",
            theme="light",
            widgets_enabled=["directory", "favorites"]
        )
        db.add(teacher_prefs)
    
    await db.commit()


async def create_default_config(db: AsyncSession):
    """Create default application configuration."""
    configs = [
        {
            "key": "school_name",
            "value": "École Exemple",
            "description": "Nom de l'établissement"
        },
        {
            "key": "academic_year",
            "value": "2024-2025",
            "description": "Année scolaire"
        },
        {
            "key": "periods",
            "value": [
                {"name": "Trimestre 1", "start": "2024-09-01", "end": "2024-12-20"},
                {"name": "Trimestre 2", "start": "2025-01-06", "end": "2025-04-05"},
                {"name": "Trimestre 3", "start": "2025-04-22", "end": "2025-07-04"}
            ],
            "description": "Périodes de l'année scolaire"
        },
        {
            "key": "schedule_settings",
            "value": {
                "start_hour": "08:00",
                "end_hour": "17:00",
                "weeks_type": "AB"
            },
            "description": "Paramètres de l'emploi du temps"
        }
    ]
    
    for config_data in configs:
        result = await db.execute(
            select(AppConfig).where(AppConfig.key == config_data["key"])
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            config = AppConfig(**config_data)
            db.add(config)
    
    await db.commit()


async def bootstrap_database(db: AsyncSession):
    """Bootstrap database with initial data."""
    await create_default_users(db)
    await create_default_config(db)
