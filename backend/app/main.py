from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, config, dashboard, notifications, protocols, reports, schedule, seating, students
from .core.config import get_settings
from .database import init_db
from .services.bootstrap import bootstrap_defaults

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in settings.backend_cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(schedule.router)
app.include_router(dashboard.router)
app.include_router(protocols.router)
app.include_router(config.router)
app.include_router(seating.router)
app.include_router(reports.router)
app.include_router(notifications.router)


@app.on_event("startup")
async def startup_event() -> None:
    await init_db()
    await bootstrap_defaults()
