from fastapi import FastAPI
from routers import manager

app = FastAPI()

app.include_router(manager.router)


app = FastAPI()


