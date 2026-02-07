from django.db import models

# Create your models here.


class Department(models.Model):
    title = models.CharField(max_length=100)

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    cv = models.FileField(null=True, blank=True)

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_quantity = models.IntegerField()

class Picture(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images")
