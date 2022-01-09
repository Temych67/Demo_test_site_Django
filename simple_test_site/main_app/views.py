from django.shortcuts import render, redirect, reverse
from main_app.forms import RegistrationForm,AuthenticattionForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from main_app.models import User_Custom_Model

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('main_app_templates/activation_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_HOST_USER,
                         to=[user.email]
                         )

    EmailThread(email).start()

def index(request):
    context = {}
    return render(request, 'main_app_templates/home_page.html', context)


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            send_activation_email(account, request)
            # login(request, account)
            return render(request, 'main_app_templates/email_template.html')
        else:
            context['registration_form'] = form
    # request.GET
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'main_app_templates/registration.html', context)

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AuthenticattionForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if not user.is_email_verified:
                return render(request, 'main_app_templates/email_template.html')
            elif user:
                login(request, user)
                return redirect('home_page')
    else:
        form = AuthenticattionForm()

    context['login_form'] = form
    return render(request, 'main_app_templates/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('home_page')

def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User_Custom_Model.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))

    return render(request, 'authentication/activate-failed.html', {"user": user})
