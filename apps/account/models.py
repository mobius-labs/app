from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Models related to accounts, and the registration and logging in of users.

# Manages the creation of users or superusers.
from apps.contact_book.models import Contact


class AccountManager(BaseUserManager):

    # registers a new user, as per user email login and password, and returns that User object
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User did not enter an email address.")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # creates an administrative 'superuser' (to be reserved for developers), returns it as User object
    def create_superuser(self, email,  password):
        if not email:
            raise ValueError("User did not enter an email address.")

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Models a user of the app, or developer/superuser of the app
class User(AbstractBaseUser):
    email = models.EmailField(max_length=50, primary_key=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    connected_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)
    business_card = models.BooleanField(default=False)
    # business_card_url = models.CharField(max_length=10)

    # the field the user logs in with
    USERNAME_FIELD = 'email'

    objects = AccountManager()

    def __str__(self):
        return self.email

    # can ignore for MVP sprint
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


# Creates an authentication token, to be used for API calls, access to user's database, for now and future sessions.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)





