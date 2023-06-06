from django.contrib import admin
from .models import *

# Register your models here.
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'email', 'phone')
    ordering = ["-date_created"]
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'request_date', 'status', 'appointment_date', 'appointment_time')
    ordering = ["request_date"]
    def appointment_time(self, obj):
        return obj.strftime("%H:%M")
admin.site.register(Appointment, AppointmentAdmin)

class PresciptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'name', 'medicine_type', 'duration', 'usage')
admin.site.register(Prescription, PresciptionAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ['date_created']
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'price', 'stock')
    ordering = ['date_created']
admin.site.register(Product, ProductAdmin)


class SalesAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'price', 'qty', 'total']
admin.site.register(Sales, SalesAdmin)