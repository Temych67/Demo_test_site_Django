from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'main_app/home_page.html', context)
