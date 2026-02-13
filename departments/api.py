from ninja import Router, NinjaAPI
from typing import List

from employees.schema import EmployeeOut
from .schema import DepartmentIn, DepartmentOut
from .models import Department
from django.shortcuts import get_object_or_404



api = NinjaAPI()

router = Router(tags=["Departments"])
employees_router = Router(tags=["Employees"])

@router.post("/", response=DepartmentOut)
def create_department(request, payload: DepartmentIn):
    department = Department.objects.create(**payload.dict())
    return department

@router.get("/", response=List[DepartmentOut])
def get_departments(request):
    return Department.objects.all()

@router.get("/{department_id}", response=DepartmentOut)
def get_department(request, department_id: int):
    department = get_object_or_404(Department, id=department_id)
    return department

from employees.schema import EmployeeOut
@employees_router.get("/", response=List[EmployeeOut])
def list_department_employees(request, department_id: int):
    from employees.models import Employee
    return Employee.objects.filter(department_id=department_id)

# Nested api example
#api.add_router("/departments/", department_router)
router.add_router("/{department_id}/employees/", employees_router)