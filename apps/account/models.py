from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

# this is where we create our user
class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User did not enter an email address.")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username,  password):
        if not email:
            raise ValueError("User did not enter an email address.")

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
        # add staff and admin too ?


class User(AbstractBaseUser):
    email = models.CharField(max_length=50, primary_key=True)
    username = models.CharField(max_length=30, unique=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # linkedToContactId = models.OneToOneField('Contact', on_delete=models.CASCADE)
    # more user fields

    # the field the user logs in with
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
        return self.email

    # can ignore for now
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True





