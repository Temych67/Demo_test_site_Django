from django.shortcuts import render, redirect
from main_app.forms import RegistrationForm,AuthenticattionForm
from django.contrib.auth import login, authenticate, logout

def index(request):
    context = {}
    return render(request, 'main_app/home_page.html', context)


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home_page')
        else:
            context['registration_form'] = form
    # request.GET
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'main_app/registration.html', context)

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

            if user:
                login(request, user)
                return redirect('home_page')
    else:
        form = AuthenticattionForm()

    context['login_form'] = form
    return render(request, 'main_app/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('home_page')

