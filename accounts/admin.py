from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import User
from .forms import CustomUserCreationForm

# Register your models here.
# class CustomUserAdmin(UserAdmin):
#     # Making password field non-editable
#     fieldsets = []
#     filter_horizontal = []
#     list_filter = []

#     # changing the display menu of User model at admin panel
#     list_display = ['email', 'first_name', 'last_name', 'is_active']

#     # ordering the list of users depending on the date_joined field descending
#     ordering = ['-date_joined']
    


# admin.site.register(User, CustomUserAdmin)



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
        ['Permissions', {'fields': ['is_admin', 'is_staff', 'is_active', 'is_superadmin',]}],
        ['Important dates', {'fields': ['date_joined', 'created_at', 'updated_at', 'last_login',]}],
    ]

    add_fieldsets = [
        [None, {
            'classes': ['wide',],
            'fields': ['email', 'password', 'confirm_password', 'first_name', 'last_name', 'phone_number', 'role', 'is_active']},
        ],
    ]

admin.site.register(User, CustomUserAdmin)
