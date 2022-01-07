from django.contrib import admin
from main_app.models import Account
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
	list_display = ('username','email','is_admin')
	search_fields = ('username','email')


	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Account, AccountAdmin)