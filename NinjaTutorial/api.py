from ninja import NinjaAPI, Schema
from .schema import HelloSchema, UserSchema, Error
from users.api import router as users_router
from departments.api import router as department_router
from employees.api import router as employee_router
from ninja.security import django_auth
from .auth import BasicAuth
from functools import wraps
from ninja import Redoc
from ninja import Swagger
from django.contrib.admin.views.decorators import staff_member_required
from users.exceptions import ServiceUnavailableError

api = NinjaAPI(servers=[{"url": "https://stag.example.com", "description": "Staging Env"}, {"url": "https://prod.example.com", "description": "Production Env"}],docs=Swagger(settings={"filter": True,}), title="Django Ninja Demo API", description="This is a demo API with dynamic OpenAPI info section")

#@api.exception_handler(ServiceUnavailableError)
#def service_unavailable(request, exc):
#    return api.create_response(request, {"message": "Please retry later"}, status=503,)


def log_operation(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(request, *args, **kwargs)
        print(f"Result: {result}")
        return result
    return wrapper

api.add_decorator(log_operation, mode="view")
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
#users_url = reverse_lazy("api-1.0.0:user_list")

api.add_router("/users/", users_router)
api.add_router("/employees/", employee_router)
api.add_router("/departments/", department_router)