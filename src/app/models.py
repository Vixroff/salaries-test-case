import uuid

from sqlalchemy import UUID, Column, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from database import Base


class Salary(Base):
    __tablename__ = 'salaries'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    salary = Column(Numeric(precision=10, scale=2))
    increase_date = Column(Date)

    employee_id = Column(UUID, ForeignKey('users.id', ondelete='CASCADE'), index=True)
    employee = relationship('Employee', back_populates='salary')


from users.models import Employee

Employee.salary = relationship('Salary', uselist=False, back_populates='employee')
