from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserChangeForm

from .models import User
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User

    # Making password field non-editable
    fieldsets = []
    filter_horizontal = []
    list_filter = []


    list_display = ['email', 'is_staff', 'is_active','last_login',]
    list_filter = ['role',]
    ordering = ['email',]
    search_fields = ['email', 'first_name', 'last_name',]
    readonly_fields = ['date_joined', 'created_at', 'updated_at', 'last_login',]


    fieldsets = [
        [None, {'fields': ['email', 'password', 'first_name', 'last_name', 'username', 'phone_number', 'role']}],
        ['Permissions', {'fields': ['is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',]}],
        ['Important dates', {'fields': ['date_joined', 'created_at', 'updated_at', 'last_login',]}],
    ]

    add_fieldsets = [
        [None, {
            'classes': ['wide',],
            'fields': ['email', 'password', 'confirm_password', 'first_name', 'last_name', 'phone_number', 'role', 'is_active', 'groups', 'user_permissions',]},
        ],
    ]

admin.site.register(User, CustomUserAdmin)

admin.site.register(Permission)
