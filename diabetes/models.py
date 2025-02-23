from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Creates a custom user model (django uses username as the default identifier instead of email).
# also disables username entirely since it's not needed.
# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None, terms_accepted=False, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, terms_accepted=terms_accepted, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name=None, last_name=None, terms_accepted=True, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, first_name, last_name, terms_accepted, **extra_fields)

# Custom User Model
class User(AbstractUser):
    username = None  # Remove username field
    is_staff = models.BooleanField(default=False)  # Define explicitly
    is_superuser = models.BooleanField(default=False)  # Define explicitly
    email = models.EmailField(unique=True)
    terms_accepted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "terms_accepted"]

    objects = CustomUserManager()  # Assign the custom manager

    def __str__(self):
        return self.email

class Diagnosis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pregnancies = models.IntegerField()
    glucose = models.FloatField()
    blood_pressure = models.FloatField()
    skin_thickness = models.FloatField()
    insulin = models.FloatField()
    bmi = models.FloatField()
    diabetes_pedigree_function = models.FloatField()
    age = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    has_diabetes = models.BooleanField()

    def __str__(self):
        return f"{self.user.first_name} - {self.diagnosis}"