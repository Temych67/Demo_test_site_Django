from django.contrib import admin
from main_app.models import User_Custom_Model
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_admin')
    search_fields = ('username', 'email')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User_Custom_Model, UserAdmin)
