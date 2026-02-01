from datetime import date
from ninja import Schema
from typing import Optional
from ninja.orm import ModelSchema
from .models import Employee, Item

# Schema for creation of Employees
class EmployeeIn(Schema):
    first_name: str | None = None
    last_name: str | None = None
    department_id: int | None = None
    birthdate: date | None = None

# Schema for handling how employee details will be sent to the client
class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    department: DepartmentOut
   # department_title: str
    birthdate: date = None

# Schema for creating departments
class DepartmentIn(Schema):
    id: int
    title: str
# Schema for handling Department api output to the client
class DepartmentOut(Schema):
    id: int
    title: str
# Schema for handling Employee incoming search request
class EmployeeSearchSchema(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
# Schema for handling how the Employee Search will be sent to the API client
class EmployeeOutSchema(ModelSchema):
    class Meta:
        model = Employee
        fields = "__all__"

# Schema for handling items that are being created
class ItemIn(Schema):
    item_name: str
    item_description: Optional[str]
    item_price: float
    item_quantity: int

# Schema for handling  how items will be sent to the client API
class ItemOut(Schema):
    id: int
    item_name: str
    item_description: str
    item_price: float
    item_quantity: int