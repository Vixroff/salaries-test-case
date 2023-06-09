import uuid
import bcrypt

from sqlalchemy import Column, UUID, String, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship

from database import Base


# class Employee(Base):
#     __tablename__ = 'employees'

#     id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
#     username = Column(String(50), unique=True, nullable=False)
#     password = Column(String, nullable=False)

#     salary = relationship('Salary', back_populates='employee')

#     def set_password(self, password: str):
#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#         self.password = hashed_password.decode('utf-8')
    
#     def verify_password(self, password: str):
#         return bcrypt.checkpw(password.encode('utf-8'), self.password)


class Salary(Base):
    __tablename__ = 'salaries'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    salary = Column(Numeric(precision=10, scale=2))
    increase_date = Column(Date)

    # employee_id = Column(UUID, ForeignKey('employees.id', ondelete='CASCADE'), index=True)
    # employee = relationship('Employee', back_populates='salary')
