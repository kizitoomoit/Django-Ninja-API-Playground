from ninja import Router
from typing import List
from .schema import DepartmentIn, DepartmentOut
from .models import Department
from django.shortcuts import get_object_or_404





router = Router(tags=["Departments"])

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