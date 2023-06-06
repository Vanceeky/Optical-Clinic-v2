from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

class Patient(models.Model):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length = 255, null = True)
    lastname = models.CharField(max_length = 255, null = True)  
    age = models.CharField(max_length = 255, null = True)  
    email = models.CharField(max_length = 255, null = True)

    gender = models.CharField(max_length=6, null = True, blank = True, choices = gender_choices)
    phone = models.CharField(max_length = 11, null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    

class Appointment(models.Model):
    Status = (
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
    )

    patient = models.OneToOneField(Patient, null = True, on_delete = models.CASCADE)

    message = models.TextField(max_length=255, null = True, blank = True)
    request_date = models.DateField(auto_now_add=False, null = True)

    sent_date = models.DateField(auto_now_add=True)
    
    status = models.CharField(max_length = 255, choices = Status, default = 'Pending')

    appointment_date = models.DateField(auto_now_add=False, null=True, blank = True)
    
    appointment_time = models.TimeField(auto_now_add = False, null = True, blank = True)

    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return f'{self.patient}' 
    

class Prescription(models.Model):

    patient = models.ForeignKey(Patient, null = True, on_delete = models.CASCADE)

    name = models.CharField(max_length = 255, null = True)
    medicine_type = models.CharField(max_length = 255, null = True)
    duration = models.CharField(max_length = 255, null = True)
    usage = models.CharField(max_length = 255, null = True)

    comment = models.TextField(max_length=255, null = True, blank = True)

    date_start = models.DateField(null = True, blank = True)
    date_end = models.DateField(null = True, blank = True)

    def __str__(self):
        return f'{self.patient} - { self.name }'



    

class Category(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to = 'category_image', null = True, blank = True)

    description = models.TextField()
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, null = True, on_delete=models.CASCADE)
    code=models.CharField(max_length=100,blank=True, null=True)
    name=models.CharField(max_length=250,blank=True, null=True)
    image = models.ImageField(upload_to = 'product_image', null = True, blank = True)

    description = models.TextField()
    price = models.FloatField(default=0)
    stock = models.FloatField(default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Sales(models.Model):

    product = models.ForeignKey(Product, null = True, blank = True, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)

    date_created = models.DateTimeField(auto_now_add=True, null = True, blank = True)

    def __str__(self):
        return f'{self.id} - { self.product }'


