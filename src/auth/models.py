from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    
    username = Column(String(50), nullable=False)
    salary = relationship('Salary', back_populates='employee')

