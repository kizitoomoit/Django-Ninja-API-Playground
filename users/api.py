from ninja import Router
from .schema import UserIn, LoginSchema
from django.contrib.auth.models import User


router = Router(tags=["Users"])

@router.post("/")
def create_user(request, payload: UserIn):
    user = User(username=payload.username, email=payload.email)
    user.set_password(payload.password)