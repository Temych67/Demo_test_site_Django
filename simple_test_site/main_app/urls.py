from django.urls import path

from main_app import views

urlpatterns = [
    path('', views.index, name='home_page'),
    #
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.logout_view, name='logout')
]