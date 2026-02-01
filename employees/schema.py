from datetime import date
from ninja import Schema
from typing import Optional
from ninja.orm import ModelSchema
from .models import Employee, Item

class EmployeeIn(Schema):
    first_name: str | None = None
    last_name: str | None = None
    department_id: int | None = None
    birthdate: date | None = None

class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    department: DepartmentOut
   # department_title: str
    birthdate: date = None

class DepartmentIn(Schema):
    id: int
    title: str

class DepartmentOut(Schema):
    id: int
    title: str

class EmployeeSearchSchema(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class EmployeeOutSchema(ModelSchema):
    class Meta:
        model = Employee
        fields = "__all__"

class ItemIn(Schema):
    item_name: str
    item_description: Optional[str]
    item_price: float
    item_quantity: int

class ItemOut(Schema):
    id: int
    item_name: str
    item_description: str
    item_price: float
    item_quantity: int