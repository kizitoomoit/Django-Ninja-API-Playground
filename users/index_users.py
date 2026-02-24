import os
import django
import asyncio
import sys
from asgiref.sync import sync_to_async
from datetime import datetime

from django.contrib.auth import get_user_model

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django Settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NinjaTutorial.settings")
django.setup()
from django.contrib.auth.models import User
from elasticsearch import AsyncElasticsearch

User = get_user_model()
es = AsyncElasticsearch("http://localhost:9200")

async def index_users():
    #users = await sync_to_async(lambda: list(User.objects.all()))()
    users = await sync_to_async(list)(User.objects.all())
    for user in users:
        await es.index(
            index="users",
            id=user.id,
            document={
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "date_joined": user.date_joined.isoformat()
            }
        )
    await es.close()
asyncio.run(index_users())
