from ninja import NinjaAPI, Schema
from .schema import HelloSchema, UserSchema, Error
from employees.api import router as employee_router
from departments.api import router as department_router

api = NinjaAPI()

#class HelloSchema(Schema):
#    name: str = "world"
#@api.post("/hello")
#def hello(request, data: HelloSchema):
#    return f"Hello, {data.name}!"
#
#@api.get("/math/{a}and{b}")
#def math(request, a: int, b: int):
#    return {"add": a + b, "multiply": a * b}
#
#@api.get("/me", response={200: UserSchema, 403: Error})
#def me(request):
#    if not request.user.is_authenticated:
#        return 403, {"message": "Please sign in first"}
#    return request.user
#

api.add_router("/employees/", employee_router)
api.add_router("/departments/", department_router)