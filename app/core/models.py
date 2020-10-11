from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have a valid email address')
        # creates the new user model - this corresponds to the User class below
        # NOT fully clear how atm
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # sets the password
        user.set_password(password)
        # saves the model to some database
        user.save(using=self._db)
        # returns the just created user model
        return user

    # this is actually going to be used for the python manage.py createsuperuser command
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    # these are all class fields - i.e. static variables
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BigIntegerField(default=True)
    is_staff = models.BooleanField(default=False)

    user_manager = UserManager()

    USERNAME_FIELD = 'email'

