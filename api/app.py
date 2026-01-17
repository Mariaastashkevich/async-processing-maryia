from fastapi import FastAPI
from api.routes.job import router as datasets_router

def create_app() -> FastAPI:
    fastapi_app = FastAPI(title="Asynchronous Data Processing API")
    fastapi_app.include_router(
        datasets_router,
        prefix='/datasets',
        tags=['datasets'],
    )
    return fastapi_app

