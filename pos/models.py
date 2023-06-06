from django.db import models
from django.utils import timezone
from dashboard.models import Product

# Create your models here.

""" class Sales(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.code
     """
class salesItems(models.Model):
    #sale_id = models.ForeignKey(Sales,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return self.sale_id
