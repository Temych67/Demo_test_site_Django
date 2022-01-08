from django.shortcuts import render, redirect
from main_app.forms import RegistrationForm
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


def logout_view(request):
    logout(request)
    return redirect('home_page')

