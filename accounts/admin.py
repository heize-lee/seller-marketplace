# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('date_joined', 'is_staff', 'email', 'nickname', 'phone_number', 'profile_picture', 'role', 'is_active')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
