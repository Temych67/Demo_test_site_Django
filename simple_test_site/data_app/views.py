from django.shortcuts import render, redirect, get_object_or_404
from data_app.models import DataModels
from data_app.forms import CreateDataPostForm, UpdateDataPostForm
from main_app.models import User_Custom_Model
from django.http import HttpResponse



def create_data_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('home_page')

    form = CreateDataPostForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        author = User_Custom_Model.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateDataPostForm()
        context['success_message'] = "Create"
    context['form'] = form

    return render(request, 'data_templates/create_data.html', context)


def detail_data_view(request, slug):
    context = {}

    data_post = get_object_or_404(DataModels, slug=slug)
    context['data_post'] = data_post

    return render(request, 'data_templates/detail_data.html', context)


def edit_data_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('home_page')

    data_post = get_object_or_404(DataModels, slug=slug)

    if data_post.author != user:
        return HttpResponse('You are not the author of that post.')

    if request.POST:
        form = UpdateDataPostForm(request.POST or None, request.FILES or None, instance=data_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            data_post = obj

    form = UpdateDataPostForm(
        initial={
            "title": data_post.title,
            "body": data_post.body,
        }
    )

    context['form'] = form
    return render(request, 'data_templates/edit_data.html', context)


def delete_date_view(request, slug):
    context = {}
    data_post = get_object_or_404(DataModels, slug=slug)

    user = request.user
    if not user.is_authenticated:
        return redirect('home_page')
    if data_post.author != user:
        return HttpResponse('You are not the author of that post.')

    if request.POST:
        data_post.delete()
        return redirect('home_page')
    context['data_post'] = data_post
    return render(request, 'data_templates/delete_data.html', context)
