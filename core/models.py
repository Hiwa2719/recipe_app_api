from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager as BaseManager
from django.db import models


class UserManager(BaseManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('users must have an email address')
        if not password:
            raise ValueError('users must have a password')

        instance = self.model(
            email=email.lower(),
            **extra_fields
        )
        instance.set_password(password)
        instance.save()
        return instance

    def create_superuser(self, email=None, password=None, **extra_fields):
        if not extra_fields.setdefault('is_staff', True):
            raise ValueError('is_staff must be True')
        if not extra_fields.setdefault('is_superuser', True):
            raise ValueError('is_superuser must be True')

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='email address')
    name = models.CharField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='active')
    is_staff = models.BooleanField(default=False, verbose_name='staff status')
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_superuser


class TagIngredient(models.Model):
    name = models.CharField(max_length=256, unique=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Tag(TagIngredient):
    pass


class Ingredient(TagIngredient):
    pass


class Recipe(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=256)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    link = models.CharField(max_length=256, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
