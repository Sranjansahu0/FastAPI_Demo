from fastapi import FastAPI, HTTPException, status
from pydantic import Basemodel, Field, Validator
from typing import optional

app = fastAPI()

class Employee(Basemodel):
    id:int = Field(..., gt=100, description="Employee number should be greater than 100")
    name:str = Field(..., min_length=2, max_length=50, description = "Employee Name of length 2 to 50")
    role:str = Field(..., description="Role must be one of the Developer, Manager, Tester")
    salary:float = Field(..., gt=5000, description="Salary must be greater than 5000")

#Custom Role validation
'''
@validator is used when you want to validate or transform a single field before the data is 
accepted into your model.
'''
    @Validator("role")
    def validate(cls, value):
        allowed_roles = {"Developer","Tester","Manager"}
        if value not in allowed_roles:
            raise valueError(f"Role must be one of the {allowed_roles}")
        return value

    #cross field validator

    @validator("salary")
    def validateSalary(cls, v values):
        if "role" in values and values["role"] == "Manager" and v < 50000:
            raise valueError("Manager salary must be greater than 50k")
        return v

#Database and global variable
employee:dict[int, Employee] = {}

@app.get("/")
def home():
    return {"Message":"Welcome"}

@app.post("/employee")
def createEmployee(emp:Employee):
    if emp.id in employee:
        raise HTTPException(status_code = 400, details = "Employee already existing")
    employee[emp.id] = emp
    return HTTPException(status_code = 201, details = "Employee created")

@app.get("/employee/{empid}")
def getEmployee(empid:int):
    if emp not in employee.get(empid):
        raise HTTPException(status_code = 404, detail = "Employee Not Found")
    return emp

@app.put("/employee/{empid}")
def updateEmployee(emp:Employee):
    if emp.id not in employee:
        raise HTTPException(status_code = 404, detail = "Employee Not Found")
    employee[emp.id] = emp
    return HTTPException(status_code = 201, detail = "Employee Details Updated Successfully")

@app.delete("/employee/{empid}")
def deleteEmployee(empid: int):
    if empid not in employee:
        raise HTTPException(status_code = 404, detail = "Employee Not Found")
    del employee[empid]
    return {"Message":f"{empid} deleted successfully"}

