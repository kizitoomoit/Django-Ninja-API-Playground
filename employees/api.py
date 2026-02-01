from .schema import EmployeeIn, EmployeeOut, DepartmentIn, DepartmentOut, EmployeeOutSchema, EmployeeSearchSchema, ItemIn, ItemOut
from ninja import NinjaAPI
from .models import Employee, Department, Item
from ninja import UploadedFile, File, Query
from django.shortcuts import get_object_or_404
from typing import List
from .services import list_employees, employee_details, update_employee_details, create_new_employee, delete_employee_api, search_employee
from ninja import router

api = NinjaAPI()

# Create employees
@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: File[UploadedFile]):
    employee = create_new_employee(payload, cv)
    return {"id": employee.id}
   # payload_dict = payload.dict()
   # employee = Employee(**payload_dict)
   # employee.cv.save(cv.name, cv) # Will save model instance as well
   # #employee = Employee.objects.create(**payload.dict())
   # return {"id": employee.id}

# This is endpoint is responsible for employees using their first name or last name
@api.get("/employees/search", response=List[EmployeeOutSchema])
def search_for_employee(request, filters: Query[EmployeeSearchSchema]):
    return search_employee(filters)

# Get employees details
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    #employee = get_object_or_404(Employee, id=employee_id)
    #return employee
    employee =  employee_details(employee_id)
    return employee


# Get list of employees
@api.get("/employees", response=List[EmployeeOut])
def get_employees(request):
    employee = list_employees()
    return employee
    #qs = Employee.objects.all()
    #return qs
   # employees = Employee.objects.select_related("department").all()
   # result = []
   # for employee in employees:
   #     result.append(EmployeeOut(id=employee.id, first_name=employee.first_name, last_name=employee.last_name, department_id=employee.department_id, department_title=employee.department.title, birthdate=employee.birthdate))

   # return result


# Update Employee
@api.put("/employees/{employee_id}", response=EmployeeOut)
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = update_employee_details(employee_id, payload)
    #employee = get_object_or_404(Employee, id=employee_id)
    #for attr, value in payload.dict().items():
    #    setattr(employee, attr, value)
    #employee.save()
    return employee

# This api endpoint is responsible for deleting employee using their id
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = delete_employee_api(employee_id)
    return {"success": True}

# This api endpoint is responsible for creating new departments
@api.post("/departments")
def creat_department(request, payload: DepartmentIn):
    department = Department.objects.create(**payload.dict())
    return {"id": department.id }

# This api endpoint is responsible for getting a single employee using their id
@api.get("/departments/{department_id}", response=DepartmentOut)
def get_department(request, department_id: int):
    department = get_object_or_404(Department, id=department_id)
    return department

# This api endpoint is responsible for listing departments
@api.get("/departments", response=List[DepartmentOut])
def get_departments(request):
    qs = Department.objects.all()
    return qs

# This is a mock data for the weapons api endpoint
weapons = ["Ninjato", "Shuriken", "katana", "Kama", "Kunai", "Naginata", "Yari"]

# This endpoint is responsible for listing available weapons, with limit and offset capabilities
@api.get("/weapons")
def list_weapons(request, limit: int, offset: int):
    return weapons[offset: offset + limit]


# This endpoint is responsible for fetching available items
@api.get("/items", response=List[ItemOut])
def get_items(request):
    item = Item.objects.all()
    return list(item)


# This endpoint is responsible for creating items
@api.post("/items", response=ItemOut)
def create_items(request, payload: ItemIn):
    item = Item.objects.create(**payload.dict())
    return item

# This endpoint is repsonsible for deleting item
@api.delete("/items/{item_id}")
def delete_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return {"Success": True}
