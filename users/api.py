from typing import Optional, Any

from django.http import HttpRequest
from ninja import Router
from .schema import UserIn, LoginSchema
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from ninja.decorators import decorate_view
from functools import wraps
import time
import asyncio
from ninja.security import HttpBearer
from ninja.security import APIKeyHeader
from ninja.security import SessionAuth

def universal_decorator(func):
    if asyncio.iscoroutinefunction(func):
        # Handle Async functions
        @wraps(func)
        async def async_wrapper(request, *args, **kwargs):
            # Async logic here
            result = await func(request, *args, **kwargs)
            if isinstance(result, dict):
                result["decorated"] = True
                result["type"] = "async"
            return result
        return async_wrapper
    else:
    # Handle sync functions
        @wraps(func)
        def sync_wrapper(request, *args, **kwargs):
            # sync logic here
            result = func(request, *args, **kwargs)
            if isinstance(result, dict):
                result["decorated"] = True
                result["type"] = "sync"
            return result
        return sync_wrapper





def timing_decorator(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        start = time.time()
        result = func(request, *args, **kwargs)
        duration = time.time() - start
        if isinstance(result, dict):
            result["_timing"] = f"{duration:.3f}s"
        return result
    return wrapper

router = Router(tags=["Users"])
router.add_decorator(universal_decorator)



#router.add_decorator(log_operation) # OPERATION mode by default

@router.post("/")
def create_user(request, payload: UserIn):
    user = User(username=payload.username, email=payload.email)
    user.set_password(payload.password)

@router.get("/")
def list_users(request):
    """Returning all users"""
    print(list_users.__name__)
    return {"users": ["Alice", "Bob", "Caro"]}

@router.get("/cached")
@decorate_view(cache_page(60 * 2))
def cached_endpoint(request):
    return {"data": "This response is cached for 2 minutes"}

@router.get("async")
async def async_endpoint(request):
    await asyncio.sleep(5)
    return {"endpoint": "async"}
@router.get("/sync")
def sync_endpoint(request):
    return {"endpoint": "sync"}

# Authentication examples

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token
@router.get("/bearer", auth=AuthBearer())
def bearer(request):
    return {"token": request.auth}

# API Key
class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        if key == "supersecret":
            return key

header_key = ApiKey()

@router.get("/headerkey", auth=header_key)
def apikey(request):
    return f"Token = {request.auth}"

# Session Authentication
@router.get("/protected", auth=SessionAuth())
def protected_view(request):
    return {"user": request.auth.username}