from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db, async_session_maker
from app.services.bootstrap import bootstrap_database
from app.api import auth, students, schedule, dashboard, seating, protocols, config, evaluations, reminders, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    await init_db()
    
    # Bootstrap initial data
    async with async_session_maker() as session:
        await bootstrap_database(session)
    
    yield
    
    # Shutdown
    pass


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(schedule.router)
app.include_router(dashboard.router)
app.include_router(seating.router)
app.include_router(protocols.router)
app.include_router(config.router)
app.include_router(evaluations.router)
app.include_router(reminders.router)
app.include_router(reports.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to LogiSuiEl School Management API",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
