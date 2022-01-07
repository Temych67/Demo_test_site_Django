from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'main/home_page.html', context)
