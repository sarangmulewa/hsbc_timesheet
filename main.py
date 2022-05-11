import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

import utils
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HSBC Timesheet", description="FastAPI based project", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/employee/", response_model=list[schemas.Employee])
def get_employees(page: int = 0, page_size: int = 10, db: Session = Depends(get_db)):
    """
        Fetch all the Employees
    """
    employees = utils.get_employees(db, page=page, page_size=page_size)
    return employees


@app.get("/employee/{employee_id}/", response_model=schemas.Employee)
def get_employee_by_id(employee_id: str, db: Session = Depends(get_db)):
    """
        Fetch Employee by Employee ID
    """
    db_employee = utils.get_employee_by_id(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@app.post("/employee/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    """
        Create Employee Record
    """
    db_employee = utils.get_employee_by_id(db, employee_id=employee.employee_id)
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee already registered")
    return utils.create_employee(db=db, employee=employee)


@app.get("/employee/{employee_id}/timesheet/", response_model=list[schemas.Timesheet])
def get_timesheet_employee_id(
        employee_id: str, date: str = None, page: int = 0, page_size: int = 10, db: Session = Depends(get_db)
    ):
    """
        Fetch Timesheet by Employee ID or (Employee ID and Date)
    """
    if date:
        timesheets = utils.get_timesheet_by_date(
            db, employee_id=employee_id, date=date, page=page, page_size=page_size
        )
    else:
        timesheets = utils.get_timesheet(
            db, employee_id=employee_id, page=page, page_size=page_size
        )
    if timesheets is None:
        raise HTTPException(status_code=404, detail="Timesheets not found")
    return timesheets


@app.post("/employee/{employee_id}/timesheet/", response_model=schemas.Timesheet)
def create_timesheet(employee_id: str, timesheet: schemas.TimesheetCreate, db: Session = Depends(get_db)):
    """
        Create Timesheet Record
    """
    return utils.create_timesheet(db=db, employee_id=employee_id, timesheet=timesheet)


@app.put("/employee/{employee_id}/timesheet/{timesheet_id}/", response_model=schemas.Timesheet)
def update_timesheet(employee_id: str, timesheet_id: int, hours: int, db: Session = Depends(get_db)):
    """
        Update Timesheet record
    """
    return utils.update_timesheet(db=db, employee_id=employee_id, timesheet_id=timesheet_id, hours=hours)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
