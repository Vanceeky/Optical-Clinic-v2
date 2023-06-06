from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static  

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('account-profile/', views.account_profile, name='account_profile'),
    path('account-profile/update', views.update_profile, name='update_profile'),
    path('add-appointment/', views.add_appointment, name='add_appointment'),
    path('set-apppointment/<str:pk>/', views.set_appointment, name='set_appointment'),
    path('reschedule-apppointment/<str:pk>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('cancel-request/<str:pk>/', views.cancel_request, name='cancel_request'),

    path('all-request/', views.all_request, name='all_request'),
    path('pending-request/', views.pending_request, name='pending_request'),
    path('accepted-request/', views.accepted_request, name='accepted_request'),
    path('patient-list/', views.patient_list, name='patient_list'),
    path('patient-profile/<str:pk>/', views.patient_profile, name='patient_profile'),
    path('add-prescription/', views.add_prescription, name='add_prescription'),


    #INVENTORY 
    path('category-list/', views.category, name='category'),
    path('product-list/', views.product_list, name='product_list'),
    path('product-profile/<str:pk>/', views.product_profile, name="product_profile"),
    path('add-category/', views.add_category, name='add_category'),
    path('add-product/', views.add_product, name='add_product'),
    path('update-product/<str:pk>/', views.update_product, name='update_product'),
    path('delete-product/<str:pk>/', views.delete_product, name='delete_product'),

    #POS
    path('sales-list/', views.sales, name="sales"),
    path('add-sale/', views.add_sale, name='add_sale'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)