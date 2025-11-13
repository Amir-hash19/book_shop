from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin ,Group
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.db import models
import re



class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required for regular users")

        email = extra_fields.get("email")
        if email:
            extra_fields["email"] = self.normalize_email(email)

        extra_fields.setdefault("username", None)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)

        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()    
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Superuser must have a username")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        email = extra_fields.get("email")
        if email:
            extra_fields["email"] = self.normalize_email(email)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    


def validate_username_with_special_characters(value):
    if re.match(r'^[a-zA-Z0-9]*$', value):
        raise ValidationError("Username must contain at least one special charactes")
    
    check = int(value[-1])
    s = sum(int(value[i]) * (10 - i) for i in range(9))
    r = s % 11

    if (r < 2 and check != r) or (r >= 2 and check != (11 - r)):
        raise ValidationError("Invalid national ID.")
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, validators=[validate_username_with_special_characters],unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True, region='IR')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True)

    GENDER_TYPE = (
        ("female", "FEMALE"),
        ("male", "MALE")
    )

    gender = models.CharField(max_length=6, choices=GENDER_TYPE, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)





    objects = CustomUserManager()
    USERNAME_FIELD = 'phone' 
    REQUIRED_FIELDS = ['username']


    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.username
    





class AdminActivityLog(models.Model):
    admin_user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    detail = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"{self.admin_user} - {self.action} - {self.created_at}"