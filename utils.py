from sqlalchemy.orm import Session

from models import Employee, Timesheet
from schemas import EmployeeCreate, TimesheetCreate


def get_employees(db: Session, page: int = 0, page_size: int = 10):
    return db.query(Employee).offset(page).limit(page_size).all()


def get_employee_by_id(db: Session, employee_id: str):
    return db.query(Employee).filter(Employee.employee_id == employee_id).first()


def get_employee_by_email(db: Session, email: str):
    return db.query(Employee).filter(Employee.email == email).first()


def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def get_timesheet(db: Session, employee_id: str, page: int = 0, page_size: int = 10):
    return db.query(Timesheet).filter(
        Timesheet.employee_id == employee_id
    ).offset(page).limit(page_size).all()


def get_timesheet_by_date(db: Session, employee_id: str, date: str, page: int = 0, page_size: int = 10):
    return db.query(Timesheet).filter(
        Timesheet.employee_id == employee_id, Timesheet.date == date
    ).offset(page).limit(page_size).all()


def create_timesheet(db: Session, employee_id: str, timesheet: TimesheetCreate):
    db_timesheet = Timesheet(**timesheet.dict(), employee_id=employee_id)
    db.add(db_timesheet)
    db.commit()
    db.refresh(db_timesheet)
    return db_timesheet


def update_timesheet(db: Session, employee_id: str, timesheet_id: int, hours: float):
    timesheet = db.query(Timesheet).filter(
        Timesheet.employee_id == employee_id, Timesheet.id == timesheet_id
    ).first()
    timesheet.hours = hours
    db.add(timesheet)
    db.commit()
    db.refresh(timesheet)
    return timesheet
