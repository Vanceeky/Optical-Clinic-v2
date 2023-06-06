from django.urls import path
from . import views

urlpatterns = [
    path('add-order/', views.pos, name='pos-page')   ,
    path('checkout-modal', views.checkout_modal, name="checkout-modal"),
    path('save-pos', views.save_pos, name="save-pos"),
    path('sales', views.salesList, name="sales-page"),


    path('receipt', views.receipt, name="receipt-modal"),
]
