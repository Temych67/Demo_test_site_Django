from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('data/', include('data_app.urls', 'data_app')),

    # API URLS
    path('api/data/', include('data_app.api.urls', 'data_api')),
    path('api/account/', include('main_app.api.urls', 'account_api')),
]

handler404 = 'main_app.views.handler404'
