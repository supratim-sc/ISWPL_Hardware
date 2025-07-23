from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserChangeForm
from django.utils.html import format_html

from .models import User
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User

    # Making password field non-editable
    fieldsets = []
    filter_horizontal = []
    list_filter = []


    list_display = ['email', 'full_name', 'is_staff', 'is_active','last_login', 'show_profile_image']
    list_filter = ['role',]
    ordering = ['email',]
    search_fields = ['email', 'first_name', 'last_name',]
    readonly_fields = ['date_joined', 'created_at', 'updated_at', 'last_login',]

    # CUSTOM FUNCTION TO DISPLAY PROFILE_IMAGE ON THE ADMIN PANEL
    def show_profile_image(self, user):
        if user.profile_image:
            return format_html(f'<img src="{user.profile_image.url}" alt="{user.email}" width="100" height="100" style="object-fit:contain; border-radius:50%;">')


    fieldsets = [
        [None, {'fields': ['email', 'password', 'first_name', 'last_name', 'phone_number', 'role', 'profile_image',]}],
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
