from django.urls import path

from data_app import views
app_name = 'data_app'

urlpatterns = [
    path('create', views.create_data_view, name='create'),
    path('<slug>/', views.detail_data_view, name='detail'),
    path('<slug>/edit', views.edit_data_view, name='edit'),
    path('<slug>/delete', views.delete_date_view, name='delete'),
]