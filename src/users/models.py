import uuid

from sqlalchemy import UUID, Column, String

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
