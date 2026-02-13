from django.contrib.auth import authenticate
from ninja.security import HttpBasicAuth

class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = authenticate(request, username=username, password=password)
        if user:
            return user