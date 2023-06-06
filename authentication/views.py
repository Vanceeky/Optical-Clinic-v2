from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib.auth.models import Group
from django.contrib import messages
from authentication.decorators import unauthenticated_user
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from authentication.token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import JsonResponse

@unauthenticated_user
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/sign-in.html", {"form": form, "msg": msg})

@unauthenticated_user
def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if User.objects.filter(username=username).exists():
                errors = {'username': ['Username already taken.']}
                success = False
            elif password != confirm_password:
                errors = {'confirm_password': ['Passwords do not match.']}
                success = False
            else:
                user = form.save()
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Activation link has been sent to your email id'
                message = render_to_string('accounts/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.content_subtype = 'html'
                email.send()

                success = True
                errors = {}

            response_data = {'success': success, 'errors': errors}
            return JsonResponse(response_data)

        else:
            errors = form.errors
            success = False
            response_data = {'success': success, 'errors': errors}
            return JsonResponse(response_data)

    else:
        form = SignUpForm()

    return render(request, "accounts/sign-up.html", {"form": form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        patient, _ = Group.objects.get_or_create(name='patient')
        patient.user_set.add(user)

        messages.success(request, 'Thank you for your confirmation. Now you can log in to your account.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')



