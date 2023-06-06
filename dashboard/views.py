from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

import datetime

from authentication.decorators import *

from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage, message

from django.conf import settings

from django.http import JsonResponse


# Create your views here.

def handler404(request, exception):
    return render(request, '404.html', status=404)


@allowed_users(allowed_roles=['admin', 'staff'])
def index(request):
    
    appointments = Appointment.objects.all()
    sales = Sales.objects.all()
    products = Product.objects.all()


    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')
    today = datetime.date.today()
    upcoming = datetime.date.today() + datetime.timedelta(days=1)

    todays_appointment = Appointment.objects.filter(appointment_date__year = year, appointment_date__month= month, appointment_date__day = day)

    upcoming_appointment = Appointment.objects.filter(appointment_date__gt = today).order_by("-appointment_date")



    context = {
        'appointments': appointments,
        'total_appointments': appointments.count(),
        'pending_request': appointments.filter(status = 'Pending').count(),
        'todays_date': today,
        'upcoming_date': upcoming,
        'today': todays_appointment,
        'upcoming': upcoming_appointment,

        'sales': sales.count(),
        'products': products.count()
    }


    return render(request, 'dashboard/index.html', context)

@allowed_users(allowed_roles=['admin', 'staff'])
def account_profile(request):

    return render(request, 'dashboard/account_profile.html')

@allowed_users(allowed_roles=['admin', 'staff'])
def update_profile(request):
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

    return redirect('account_profile')

    
@allowed_users(allowed_roles=['admin', 'staff'])
def add_appointment(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        age = request.POST.get('age')
        phone = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        appointment_date = request.POST.get('date')
        appointment_time = request.POST.get('time')

        patient = Patient.objects.create(
            firstname=firstname,
            lastname=lastname,
            age=age,
            gender=gender,
            phone=phone,
        )

        appointment = Appointment.objects.create(
            patient=patient,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='Accepted'
        )

        messages.success(request, 'New appointment added!')

        return JsonResponse({'message': 'success'})

    return JsonResponse({'message': 'error'})



@allowed_users(allowed_roles=['admin', 'staff'])
def set_appointment(request, pk):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment-id')
        appointment_time = request.POST.get('time')

        try:
            appointment = Appointment.objects.get(id=pk)
            appointment.status = 'Accepted'
            appointment.appointment_date = appointment.request_date
            appointment.appointment_time = appointment_time
            appointment.save()

            data = {
                'fname': appointment.patient.firstname,
                'lname': appointment.patient.lastname,
                'date': appointment.request_date,
                'time': appointment.appointment_time,
            }

            message = get_template('dashboard/includes/email.html').render(data)

            email = EmailMessage(
                'About your appointment',
                message,
                settings.EMAIL_HOST_USER,
                [appointment.patient.email],
            )

            email.content_subtype = 'html'
            email.send()

            messages.success(request, 'Appointment has been saved!')
            return JsonResponse({'message': 'success'})
        except Appointment.DoesNotExist:
            pass

    return JsonResponse({'message': 'error'})

@allowed_users(allowed_roles=['admin', 'staff'])
def cancel_request(request, pk):
    if request.method == 'POST' and request.is_ajax():
        patient_id = request.POST.get('patient_id')
        appointment = Appointment.objects.get(id=pk)

        appointment.status = 'Cancelled'
        appointment.appointment_date = None
        appointment.appointment_time = None
        appointment.save()

        data = {
            'message': 'Request cancelled successfully.'
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request.'})

@allowed_users(allowed_roles=['admin', 'staff'])
def reschedule_appointment(request, pk):
    if request.method == 'POST' and request.is_ajax():
        patient_id = request.POST.get('patient_id')
        appointment = Appointment.objects.get(id=pk)

        appointment_date = request.POST.get('date')
        appointment.appointment_date = appointment_date
        appointment.save()

        data = {
            "fname": appointment.patient.firstname,
            "lname": appointment.patient.lastname,
            "date": appointment.appointment_date,
            "time": appointment.appointment_time
        }

        message = get_template('dashboard/includes/reschedule_email.html').render(data)
        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.patient.email],
        )

        email.content_subtype = "html"
        email.send()

        data = {
            'message': 'Appointment Rescheduled!',
            'patient_id': patient_id,
            'appointment': {
                'fname': appointment.patient.firstname,
                'lname': appointment.patient.lastname,
                'date': appointment.appointment_date,
                'time': appointment.appointment_time,
            }
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request.'})

@allowed_users(allowed_roles=['admin', 'staff'])
def all_request(request):
    appointments = Appointment.objects.all()

    context = {
        'appointments': appointments,
    }
    return render(request, 'dashboard/all_request.html', context)

@allowed_users(allowed_roles=['admin', 'staff'])
def pending_request(request):

    appointments = Appointment.objects.all()

    context = {
        'appointments': appointments,
    }
    return render(request, 'dashboard/pending_request.html', context)

@allowed_users(allowed_roles=['admin', 'staff'])
def accepted_request(request):

    appointments = Appointment.objects.all()

    context = {
        'appointments': appointments,
    }
    return render(request, 'dashboard/accepted_request.html', context)


@allowed_users(allowed_roles=['admin', 'staff'])
def patient_list(request):

    appointments = Appointment.objects.all()

    context = {
        'appointments': appointments,
    }
    return render(request, 'dashboard/patients.html', context)

@allowed_users(allowed_roles=['admin', 'staff'])
def patient_profile(request, pk):

    appointment = Appointment.objects.get(id = pk)
    patient = Patient.objects.get(id = appointment.patient.id)
    prescription = Prescription.objects.filter(patient = patient)
    context = {
        'appointment': appointment,
        'prescription': prescription,
    }
    return render(request, 'dashboard/patient_profile.html', context)


@allowed_users(allowed_roles=['admin', 'staff'])
def add_prescription(request):

    patient_id = request.POST.get('patient_id')

    patient = Patient.objects.get(id = patient_id)

    prescription = Prescription.objects.all()

    name = request.POST.get('name')
    medicine_type = request.POST.get('medicine_type')
    medicine_duration = request.POST.get('medicine_duration')
    medicine_usage = request.POST.get('medicine_usage')
    comment = request.POST.get('comment')
    date_start = request.POST.get('date_start')
    date_end = request.POST.get('date_end')
    
    prescription = Prescription.objects.create(
        patient = patient,
        name = name,
        medicine_type = medicine_type,
        duration = medicine_duration,
        usage = medicine_usage,
        comment = comment,
        date_start = date_start,
        date_end = date_end,

    )

    prescription.save()

    messages.success(request, 'New prescription added!')
    return redirect("patient_profile", pk=patient_id)



#INVENTORY
@allowed_users(allowed_roles=['admin', 'staff'])
def category(request):
    category = Category.objects.all()
    context = {
        'categories': category,
    }
    return render(request, 'dashboard/category.html', context)
    
@allowed_users(allowed_roles=['admin', 'staff'])
def product_list(request):
    categories = Category.objects.all().order_by('name')
    product_list = Product.objects.all()
    context = {
        'product_list': product_list,
        'categories': categories,
    }
    return render(request, 'dashboard/product_list.html', context)

def add_category(request):
    if request.is_ajax() and request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        category = Category(
            name=name,
            description=description,
            image=image
        )

        category.save()

        response_data = {
            'message': 'New category added!'
        }
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'})

@allowed_users(allowed_roles=['admin', 'staff'])
def add_product(request):
    if request.is_ajax() and request.method == 'POST':
        category_id = request.POST.get('category')
        code = request.POST.get('code')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('p_image')

        try:
            category = Category.objects.get(id=category_id)
            product = Product.objects.create(
                category=category,
                code=code,
                name=name,
                description=description,
                price=price,
                stock=stock,
                image=image,
            )

            messages.success(request, 'New Product added!')
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request'})

@allowed_users(allowed_roles=['admin', 'staff'])  
def product_profile(request, pk):
    
    categories = Category.objects.all()
    product = Product.objects.get(id = pk)

    context = {
        'categories': categories,
        'product': product,
    }
    return render(request, 'dashboard/product_profile.html', context)

@allowed_users(allowed_roles=['admin', 'staff'])
def update_product(request, pk):

    product = Product.objects.get(id = pk)

    product_id = request.POST.get('product-id')

    code = request.POST.get('code')
    name = request.POST.get('name')
    description = request.POST.get('description')
    price = request.POST.get('price')
    stock = request.POST.get('stock')
    #image = request.FILES['pimage']

    product.code = code
    product.name = name
    product.description = description
    product.price = price
    product.stock = stock
    try:
        if request.FILES['pimage']:
            product.image = request.FILES['pimage']
    except:
         pass
    product.save()

    #product.save()

    messages.success(request, 'Product is updated! ')

    return redirect('product_profile', pk = product_id)

@allowed_users(allowed_roles=['admin', 'staff'])
def delete_product(request, pk):
    product = Product.objects.get(id = pk)
    if request.method == 'POST':
        product.delete()

    messages.success(request, 'Product deleted!')
    return redirect('product_list')

@allowed_users(allowed_roles=['admin', 'staff'])
def sales(request):
    
    product_list = Product.objects.all()
    sales = Sales.objects.all()
    context = {
        'product_list': product_list,
        'sales': sales,
    }

    return render(request, 'dashboard/sales.html', context)

@allowed_users(allowed_roles=['admin', 'staff'])
def add_sale(request):
    if request.is_ajax() and request.method == 'POST':
        product_id = request.POST.get('product')
        qty = request.POST.get('qty')

        try:
            product = Product.objects.get(id=product_id)
            price = product.price
            stock = product.stock

            product.stock = int(stock) - int(qty)
            product.save()

            total = float(qty) * float(price)

            sale = Sales.objects.create(
                product=product,
                price=price,
                qty=qty,
                total=total
            )

            messages.success(request, 'New sales added!')
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request'})
