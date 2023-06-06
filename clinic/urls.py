from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send-request', views.send_request, name='send_request'),
    path('appointment/', views.view_appointment, name='appointment'),
    path('profile/', views.profile, name='profile'),
    path('profile/update', views.update_profile_patient, name='update_profile_patient'),
]
