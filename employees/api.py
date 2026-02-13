from .schema import EmployeeIn, EmployeeOut,EmployeeOutSchema, EmployeeSearchSchema, ItemIn, ItemOut, UserDetails, UserIn, UserOut, PictureSchema, Token, Message, LoginSchema, UserSchemaOut
from django.contrib.auth.models import User
from ninja import Router, Form, UploadedFile, File, Query, Schema
from .models import Employee, Item, Picture
from django.shortcuts import get_object_or_404
from typing import List
from .services import list_employees, employee_details, update_employee_details, create_new_employee, delete_employee_api, search_employee
from datetime import date
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
#from ninja import router

#api = NinjaAPI()
router = Router(tags=["Employees"])

# Create employees
#@api.post("/employees")
@router.post("/")
def create_employee(request, payload: EmployeeIn, cv: File[UploadedFile]):
    employee = create_new_employee(payload, cv)
    return {"id": employee.id}
   # payload_dict = payload.dict()
   # employee = Employee(**payload_dict)
   # employee.cv.save(cv.name, cv) # Will save model instance as well
   # #employee = Employee.objects.create(**payload.dict())
   # return {"id": employee.id}

@router.get("/test")
def test(request):
    return {"ok": True}
# This is endpoint is responsible for employees using their first name or last name
#@api.get("/employees/search", response=List[EmployeeOutSchema])
@router.get("/search", response=List[EmployeeOutSchema])
def search_for_employee(request, filters: Query[EmployeeSearchSchema]):
    return search_employee(filters)

@router.post("/login")
def login(request, username: Form[str], password: Form[str]):
    return {'username': username, 'password': '*****'}

# This api endpoint is responsible for listing departments
#@api.get("/departments", response=List[DepartmentOut])
#@router.get("/departments", response=List[DepartmentOut])
#def get_departments(request):
#    qs = Department.objects.all()
#    return qs
# Get employees details
#@api.get("/employees/{pk}", response=EmployeeOut)
@router.get("/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    #employee = get_object_or_404(Employee, id=employee_id)
    #return employee
    employee =  employee_details(employee_id)
    return employee


# Get list of employees
#@api.get("/employees", response=List[EmployeeOut])
@router.get("/", response=List[EmployeeOut])
def get_employees(request):
    #employee = list_employees()
    return list_employees()
    #qs = Employee.objects.all()
    #return qs
   # employees = Employee.objects.select_related("department").all()
   # result = []
   # for employee in employees:
   #     result.append(EmployeeOut(id=employee.id, first_name=employee.first_name, last_name=employee.last_name, department_id=employee.department_id, department_title=employee.department.title, birthdate=employee.birthdate))

   # return result


# Update Employee
#@api.put("/employees/{employee_id}", response=EmployeeOut)
@router.put("/{employee_id}", response=EmployeeOut)
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = update_employee_details(employee_id, payload)
    #employee = get_object_or_404(Employee, id=employee_id)
    #for attr, value in payload.dict().items():
    #    setattr(employee, attr, value)
    #employee.save()
    return employee

# This api endpoint is responsible for deleting employee using their id
#@api.delete("/employees/{employee_id}")
@router.delete("/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = delete_employee_api(employee_id)
    return {"success": True}

# This api endpoint is responsible for creating new departments
#@api.post("/departments")
#@router.post("/departments")
#def creat_department(request, payload: DepartmentIn):
#    department = Department.objects.create(**payload.dict())
#    return {"id": department.id }

# This api endpoint is responsible for getting a single employee using their id
#@api.get("/departments/{department_id}", response=DepartmentOut)
##@router.get("/departments/{department_id}", response=DepartmentOut)
#def get_department(request, department_id: int):
#    department = get_object_or_404(Department, id=department_id)
#    return department


# This is a mock data for the weapons api endpoint
weapons = ["Ninjato", "Shuriken", "katana", "Kama", "Kunai", "Naginata", "Yari"]

# Experimenting with Query Parameter
# This endpoint is responsible for listing available weapons, with limit and offset capabilities
#@api.get("/weapons")
def list_weapons(request, limit: int, offset: int):
    return weapons[offset: offset + limit]

# Experimenting with GET parameters type conversion
#@api.get("/example")
def example(request, s: str = None, b: bool = None, d: date = None, i: int = None):
    return [s, b, d, i]

# This endpoint is responsible for fetching available items
#@api.get("/items", response=List[ItemOut])
def get_items(request):
    item = Item.objects.all()
    return list(item)


# This endpoint is responsible for creating items
#@api.post("/items", response=ItemOut)
def create_items(request, item: ItemIn):
    item = Item.objects.create(**item.dict())
    return item

# This endpoint is responsible for deleting item
#@api.delete("/items/{item_id}")
def delete_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return {"Success": True}

#@api.post("/login")

# Uploading a single file
#@api.post("/uploadfile")
@router.post("/uploadfile")
def upload_file(request, file: File[UploadedFile]):
    data = file.read()
    return {'name': file.name, 'len': len(data)}

# Uploading array of files
#@api.post("/upload-many")
def upload_many(request, files: File[List[UploadedFile]]):
    return [f.name for f in files]


# Uploading files with extra fields
# if the data is coming from the html form
#@api.post("/create-user")
def create_user(request, payload: Form[UserDetails], file: File[UploadedFile]):
    return [payload.dict(), file.name]

# Details will come in as JSON as string and file as File
#@api.post("/create-user2")
def create_user2(request, payload: UserDetails, file: File[UploadedFile]):
    return [payload.dict(), file.name]

# Create users in the database
#@api.post("/user", response=UserOut)
def creating_user(request, payload: UserIn):
    user = User(username=payload.username, email=payload.email)
    user.set_password(payload.password)
    user.save()
    return user

# Retrieve all users ins the database
#@api.get("/users", response=List[UserSchemaOut])
def get_user(request):
    user = User.objects.all()
    return user

#@api.post("/upload-image", response=PictureSchema)
def upload_image(request, data: Form[PictureSchema], file: File[UploadedFile]):
    picture = Picture.objects.create(title=data.title, image=file)
    return picture

#@api.get("/images", response=List[PictureSchema])
def get_images(request):
    pictures = Picture.objects.all()
    return pictures

#
#@api.get("/http")
def result_django(request):
    return HttpResponse("some data")

# Redirecting using Django ridrect
#@api.get("/something")
def some_redirect(request):
    return redirect("/some-path")

#@api.post("/login1")
def login1(request, payload: LoginSchema):
    auth_not_valid = True
    negative_balance = False
    user = authenticate(request, username=payload.username, password=payload.password)
    if user:
        login1(request, user)
        return {"success": True}
    return {"message": "Invalid credentials"}
   # if auth_not_valid:
   #     return 401, {'message': 'Unauthorized'}
   # if negative_balance:
   #     return 402, {'message': 'Insufficient balance amount. Please proceed to a payment page'}
   # return 200, {'token': 'skljfdkasjflsjaklfd', 'expires': 2026-2-20}

#@api.post("/no_contet", response={204: None})
def no_contect(request):
    return 204, None


# Altering the Responses
#@api.get("/cookie")
def feed_cookiemonster(request: HttpRequest, response: HttpResponse):
    # Set cookie
    response.set_cookie("cookie", "delicious")
    # set header.
    response["X-Cookiemonster"] = "blue"
    return {"cookiemonster_happy": True}
