from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class UserManager(BaseUserManager):

    # FOR CREATING NORMAL USER
    def create_user(self, first_name, last_name, email, phone_number, username = None, password=None):
        if not email:
            raise ValueError("User must have an email")

        username = email.split('@')[0]

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            username = username,
            phone_number = phone_number,
        )

        user.set_password (password)
        user.save(using = self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, username = None, password = None):
        super_user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            username = username,
            phone_number = phone_number,
            password = password
        )

        super_user.is_active = True
        super_user.is_admin = True
        super_user.is_staff = True
        super_user.is_superadmin = True

        super_user.save(using = self._db)

        return super_user


class User(AbstractBaseUser):
    ROLE_ADMIN = 1
    ROLE_EMPLOYEE = 2
    ROLE_ENGINEER = 3

    ROLE_CHOICE = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_EMPLOYEE, 'Employee'),
        (ROLE_ENGINEER, 'Engineer'),
    )

    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255, unique = True)
    username = models.CharField(max_length = 255, unique = True)
    phone_number = models.CharField(max_length = 255, unique = True)
    
    role = models.PositiveSmallIntegerField(choices = ROLE_CHOICE, default = ROLE_EMPLOYEE)


    date_joined = models.DateTimeField(auto_now_add = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    last_login = models.DateTimeField(auto_now = True)

    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True





        