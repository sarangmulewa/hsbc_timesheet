from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)

    timesheets = relationship("Timesheet", back_populates="employee")


class Timesheet(Base):
    __tablename__ = "timesheet"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    hours = Column(Float)
    employee_id = Column(String, ForeignKey("employee.employee_id"))

    employee = relationship("Employee", back_populates="timesheets")
