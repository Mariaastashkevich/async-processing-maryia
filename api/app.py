from fastapi import FastAPI
from api.routes.dataset import router as datasets_router
from api.routes.jobs import router as jobs_router

def create_app() -> FastAPI:
    fastapi_app = FastAPI(title="Asynchronous Data Processing API")
    fastapi_app.include_router(
        datasets_router,
        prefix='/datasets',
        tags=['datasets'],
    )
    fastapi_app.include_router(
        jobs_router,
        prefix='/jobs',
        tags=['jobs'],
    )
    return fastapi_app

