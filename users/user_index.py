from django.contrib.auth import get_user_model
from .search import es

User = get_user_model()

async def index_user(user):
    await es.index(
        index="users",
        id=user.id,
        document={
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "date_joined": user.date_joined,
        }
    )