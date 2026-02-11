from ninja import Schema
from datetime import date

class DepartmentOut(Schema):
    id: int
    title: str

class DepartmentIn(Schema):
    #id: int
    title: str