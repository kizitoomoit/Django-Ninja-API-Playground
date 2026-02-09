from .models import Employee, Department
from typing import List
from django.shortcuts import get_object_or_404
from .schema import EmployeeSearchSchema, EmployeeOut
from django.db.models import QuerySet

# Get a list of employees in the system
def list_employees() -> Employee:
    employees = Employee.objects.select_related("department")
    return employees
    #return [EmployeeOut.from_orm(e) for e in employees]

# Create new employee and upload their CV as well
def create_new_employee(payload, cv) -> Employee:
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv)
    return employee

# get employee details using their id and return 404 if there is no match
def employee_details(employee_id: int) -> Employee:
    employee = get_object_or_404(Employee, id=employee_id)
    return employee

# Update partial employee details
def update_employee_details(employee_id: int, payload) -> Employee:
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(employee, attr, value)
    employee.save()
    return employee
    #return {"success": True}

# Delete the employee in the system or return 404 if no id is found
def delete_employee_api(employee_id: id) -> bool:
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return True

# Search for employees use either their first name or last name
def  search_employee(filters: EmployeeSearchSchema):
    qs = Employee.objects.all()

    if filters.first_name:
        qs = qs.filter(first_name__icontains=filters.first_name)

    if filters.last_name:
        qs = qs.filter(last_name__icontains=filters.last_name)

    return qs


