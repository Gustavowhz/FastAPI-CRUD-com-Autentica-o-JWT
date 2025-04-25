from fastapi import FastAPI
from . import models, routes, database
from .database import get_db

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(routes.router)
