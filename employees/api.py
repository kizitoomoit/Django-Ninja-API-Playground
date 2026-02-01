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

@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = delete_employee_api(employee_id)
    return {"success": True}

@api.post("/departments")
def creat_department(request, payload: DepartmentIn):
    department = Department.objects.create(**payload.dict())
    return {"id": department.id }

@api.get("/departments/{department_id}", response=DepartmentOut)
def get_department(request, department_id: int):
    department = get_object_or_404(Department, id=department_id)
    return department

@api.get("/departments", response=List[DepartmentOut])
def get_departments(request):
    qs = Department.objects.all()
    return qs

weapons = ["Ninjato", "Shuriken", "katana", "Kama", "Kunai", "Naginata", "Yari"]

@api.get("/weapons")
def list_weapons(request, limit: int, offset: int):
    return weapons[offset: offset + limit]

@api.get("/weapons/search")
def search_weapons(request, q: str, offset: int = 0):
    results = [w for w in weapons if q in w.lower()]
    return results

@api.get("/items", response=List[ItemOut])
def get_items(request):
    item = Item.objects.all()
    return list(item)
@api.post("/items", response=ItemOut)
def create_items(request, payload: ItemIn):
    item = Item.objects.create(**payload.dict())
    return item
@api.delete("/items/{item_id}")
def delete_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return {"Success": True}
