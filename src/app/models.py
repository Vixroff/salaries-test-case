import uuid
import bcrypt

from sqlalchemy import Column, UUID, String, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship

from database import Base


class Salary(Base):
    __tablename__ = 'salary'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    salary = Column(Numeric(precision=10, scale=2))
    increase_date = Column(Date)

    employee_id = Column(UUID, ForeignKey('user.id', ondelete='CASCADE'), index=True)
    employee = relationship('Employee', back_populates='salary')
