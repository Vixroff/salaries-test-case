import uuid

from sqlalchemy import UUID, Column, Date, ForeignKey, Numeric, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship

from database import Base


class User(AsyncAttrs, Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    salary = relationship('Salary', back_populates='user', uselist=False)


class Salary(AsyncAttrs, Base):
    __tablename__ = 'salaries'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    salary = Column(Numeric(precision=10, scale=2))
    increase_date = Column(Date)

    user_id = Column(UUID, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='salary')
