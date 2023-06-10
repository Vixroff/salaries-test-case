import os
import sys

from fastapi import FastAPI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)


from auth.routers import auth_router

app = FastAPI()

app.include_router(auth_router)
