from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
