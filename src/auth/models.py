from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String

from database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    
    username = Column(String(50), nullable=False, unique=True)
