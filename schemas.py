from pydantic import BaseModel


class EmployeeBase(BaseModel):
    employee_id: str
    name: str
    email: str


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    class Config:
        orm_mode = True


class TimesheetBase(BaseModel):
    date: str
    hours: float


class TimesheetCreate(TimesheetBase):
    pass


class Timesheet(TimesheetBase):
    id: int
    employee_id: str

    class Config:
        orm_mode = True
