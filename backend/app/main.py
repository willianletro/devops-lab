from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .database import engine
from .models.user import Base
from .routers import users

app = FastAPI()

Instrumentator().instrument(app).expose(app)
Base.metadata.create_all(bind=engine)

app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "DevOps Lab API"}