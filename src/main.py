from fastapi import FastAPI
from .infrastructure.database.mongodb import init_db
from .interfaces.api.users import router

app = FastAPI(
    title="User Management API",
    description="User Management API using FastAPI, MongoDB and Beanie",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(router, prefix="/api")
