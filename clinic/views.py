from django.shortcuts import render
from dashboard.models import Category, Product

from django.core.paginator import Paginator

from authentication.decorators import *

from dashboard.models import *

from datetime import datetime
from django.contrib import messages

from django.http import JsonResponse
# Create your views here.


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    if request.user.is_authenticated:

        if Patient.objects.filter(user = request.user).exists():
            patient = Patient.objects.get(user = request.user)
            prescription = Prescription.objects.filter(patient = patient).first()
            
            context = {
                'categories': categories,
                'products': products,
                'patient': patient,
                'prescriptions': prescription,
            }
            return render(request, 'clinic/index.html', context)
        else:
            context = {
                'categories': categories,
                'products': products,
            }
            return render(request, 'clinic/index.html', context)
    else:
    
        context = {
            'categories': categories,
            'products': products,
        }
        return render(request, 'clinic/index.html', context)

def send_request(request):
    appointment = Appointment.objects.all()
    patient = Patient.objects.all()

    if request.user.is_authenticated:
        request_date = request.POST.get('date')
        comment = request.POST.get('comment')

        fname = patient.filter(firstname=request.user.first_name)
        lname = patient.filter(lastname=request.user.last_name)

        if fname.exists() and lname.exists():
            return JsonResponse({'message': 'You already sent a request!'}, status=400)

        else:
            patient = Patient.objects.create(
                user=request.user,
                firstname=request.user.first_name,
                lastname=request.user.last_name,
                email=request.user.email,
            )

            appointment = Appointment.objects.create(
                patient=patient,
                request_date=request_date,
                message=comment,
            )

            return JsonResponse({'message': 'Your request is sent! We will send you an update on your email within 24 hrs'})

    else:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        request_date = request.POST.get('date')
        comment = request.POST.get('comment')

        fname = patient.filter(firstname=firstname)
        lname = patient.filter(lastname=lastname)

        if fname.exists() and lname.exists():
            return JsonResponse({'message': 'You already sent a request, please check your email for updates!'}, status=400)

        else:
            patient = Patient.objects.create(
                firstname=firstname,
                lastname=lastname,
                age=age,
                email=email,
                phone=phone_number,
            )

            appointment = Appointment.objects.create(
                patient=patient,
                request_date=request_date,
                message=comment
            )

            return JsonResponse({'message': 'Your request is sent! We will send you an update on your email within 24 hrs'})
        
def view_appointment(request):

    user = User.objects.get(username= request.user)

    if Patient.objects.filter(user=user).exists():
        return render(request, 'clinic/appointment.html')
    else:
        return render(request, 'clinic/appointment.html')



def profile(request):
    return render(request, 'clinic/account_profile.html')

def update_profile_patient(request):
    username = request.POST.get('username')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')

    user = User.objects.get(username = request.user )

    user.username = username
    user.first_name = firstname
    user.last_name = lastname
    user.email = email
    user.save()

    messages.success(request, 'User profile updated! ')

    return redirect('profile')

