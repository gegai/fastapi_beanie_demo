from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database.mongodb import init_db
from src.infrastructure.config.settings import settings
from src.interfaces.api.users import router as users_router
from src.interfaces.api.scenes import router as scenes_router


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_url=settings.openapi_url,
    debug=settings.debug
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)


@app.on_event("startup")
async def startup_event():
    await init_db()


app.include_router(users_router, prefix=settings.api_prefix)
app.include_router(scenes_router, prefix=settings.api_prefix)
