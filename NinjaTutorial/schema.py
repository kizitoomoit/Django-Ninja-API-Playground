from ninja import Schema

class HelloSchema(Schema):
    name: str = "World"

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # Unauthenticated users don't have the following fields, so provide defaults.
    email: str
    first_name: str = None
    last_name: str = None

class Error(Schema):
    message: str


