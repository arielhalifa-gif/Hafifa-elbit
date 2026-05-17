from fastapi import FastAPI

from app.routes.air_quality import router

app = FastAPI(
    title="Air Quality API"
)

app.include_router(router)