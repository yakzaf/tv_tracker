from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from user_auth.models import User
from tracker.models import Show
#
# # Register your models here.

admin.site.register(Show)
# class AccountAdmin(UserAdmin):
#     list_display = ('email', 'username', 'date_joined', 'last_login', 'is_active', 'is_admin', 'is_staff')
#     search_fields = ('email', 'username',)
#     readonly_fields = ('date_joined', 'last_login')
#
    # filter_horizontal = ()
    # list_filter = ()
#     fieldsets = ()
#
# admin.site.register(User, AccountAdmin)
