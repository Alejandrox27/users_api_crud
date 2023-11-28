from fastapi import FastAPI
from routers.router import user

app = FastAPI()

app.include_router(user)