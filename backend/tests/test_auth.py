import os
import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

os.environ["LOGISUIEL_DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

from app.main import app  # noqa: E402
from app.database import init_db  # noqa: E402
from app.services.bootstrap import bootstrap_defaults  # noqa: E402

TEST_DB = Path("test.db")


@pytest.fixture(autouse=True)
def cleanup_db():
    if TEST_DB.exists():
        TEST_DB.unlink()
    yield
    if TEST_DB.exists():
        TEST_DB.unlink()


@pytest.fixture(autouse=True)
async def setup_database():
    await init_db()
    await bootstrap_defaults()
    yield


@pytest.mark.asyncio
async def test_login_and_profile():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/auth/token",
            data={"username": "admin", "password": "admin"},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["access_token"]

        headers = {"Authorization": f"Bearer {payload['access_token']}"}
        me = await client.get("/auth/me", headers=headers)
        assert me.status_code == 200
        me_payload = me.json()
        assert me_payload["username"] == "admin"
        assert me_payload["role"] == "ADMIN"
