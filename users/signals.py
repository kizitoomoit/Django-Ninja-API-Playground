from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .user_index import index_user
import asyncio

User = get_user_model()

@receiver(post_save, sender=User)
def update_user_index(sender, instance,  **kwargs):
    asyncio.create_task(index_user(instance))