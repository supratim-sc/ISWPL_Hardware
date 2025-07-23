from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):

    # FOR CREATING NORMAL USER
    def create_user(self, first_name, last_name, email, phone_number, password=None):
        if not email:
            raise ValueError("User must have an email")

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            phone_number = phone_number,
        )

        user.set_password (password)
        user.save(using = self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, password = None):
        super_user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            phone_number = phone_number,
            password = password,
        )

        super_user.is_active = True
        super_user.is_staff = True
        super_user.is_superuser = True

        super_user.role = User.ROLE_ADMIN

        super_user.save(using = self._db)

        return super_user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_ADMIN = 'ADMIN'
    ROLE_RECEPTIONIST = 'RECEPTIONIST'
    ROLE_ADVISER = 'ADVISER'
    ROLE_ENGINEER = 'ENGINEER'

    ROLE_CHOICE = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_RECEPTIONIST, 'Receptionist'),
        (ROLE_ADVISER, 'Adviser'),
        (ROLE_ENGINEER, 'Engineer'),
    )

    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255, unique = True)
    phone_number = models.CharField(max_length = 255, unique = True)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default_user.png', blank=True, null=True )
    
    role = models.CharField(choices = ROLE_CHOICE, default = ROLE_ENGINEER)


    date_joined = models.DateTimeField(auto_now_add = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    last_login = models.DateTimeField(auto_now = True)

    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_superuser = models.BooleanField(default = False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self) -> str:
        return self.email
    
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj = None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True





        