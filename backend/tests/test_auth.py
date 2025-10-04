import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.models import User
from app.core.security import get_password_hash

# Test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_async_session_maker = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    """Override database dependency for tests."""
    async with test_async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
async def setup_database():
    """Set up test database before each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create test users
    async with test_async_session_maker() as session:
        admin_user = User(
            username="admin",
            email="admin@test.com",
            hashed_password=get_password_hash("admin"),
            role="ADMIN",
            full_name="Test Admin",
            is_active=True
        )
        teacher_user = User(
            username="test",
            email="test@test.com",
            hashed_password=get_password_hash("test"),
            role="TEACHER",
            full_name="Test Teacher",
            is_active=True
        )
        session.add(admin_user)
        session.add(teacher_user)
        await session.commit()
    
    yield
    
    # Teardown
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def admin_token(client: AsyncClient):
    """Get admin token."""
    response = await client.post(
        "/api/auth/token",
        data={"username": "admin", "password": "admin"}
    )
    return response.json()["access_token"]


@pytest.fixture
async def teacher_token(client: AsyncClient):
    """Get teacher token."""
    response = await client.post(
        "/api/auth/token",
        data={"username": "test", "password": "test"}
    )
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test successful login."""
    response = await client.post(
        "/api/auth/token",
        data={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials."""
    response = await client.post(
        "/api/auth/token",
        data={"username": "admin", "password": "wrong"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, admin_token: str):
    """Test getting current user."""
    response = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert data["role"] == "ADMIN"


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, admin_token: str):
    """Test token refresh."""
    response = await client.post(
        "/api/auth/refresh",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
