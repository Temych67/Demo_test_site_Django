from django.shortcuts import render, redirect, reverse
from main_app.forms import RegistrationForm, AuthenticattionForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from main_app.utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from main_app.models import User_Custom_Model
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from data_app.models import DataModels
from django.db.models import Q
from operator import attrgetter

DATA_POSTS_PER_PAGE = 10


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def handler404(request, *args, **kwargs):
    return render(request, 'main_app_templates/error404.html')


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = DataModels.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))


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

    # Search
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        print(request.GET.get('q', ''))
        context['query'] = str(query)

    data_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)

    page = request.GET.get('page', 1)
    data_paginator = Paginator(data_posts, DATA_POSTS_PER_PAGE)

    try:
        data_posts = data_paginator.page(page)
    except PageNotAnInteger:

        data_posts = data_paginator.page(DATA_POSTS_PER_PAGE)
    except EmptyPage:
        data_posts = data_paginator.page(data_paginator.num_pages)

    context['data_posts'] = data_posts

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
            return render(request, 'main_app_templates/email_template.html')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'main_app_templates/registration.html', context)


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home_page')

    if request.POST:
        form = AuthenticattionForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if not user.is_email_verified:
                messages.add_message(request, messages.ERROR,
                                     'Your email is not verified')
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

        return redirect(reverse('login'))

    return render(request, 'main_app/email_template.html')
