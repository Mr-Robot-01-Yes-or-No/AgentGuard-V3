from fastapi import FastAPI
from backend.api.routers import proxy, dashboard, auth
from backend.db.database import engine, Base
from backend.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proxy.router)
app.include_router(dashboard.router)
app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
