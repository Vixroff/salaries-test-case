import os
import sys

from fastapi import FastAPI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

app = FastAPI()

from app import routers
