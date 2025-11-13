from account.models import CustomUser
from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify





class BootcampCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)



    def __str__(self):
        return self.name
    



class Bootcamp(models.Model):

    BOOTCAMP_STATUS_CHOICES=(
        ("draft", "Draft"),
        ("registering", "Registering"),
        ("currently", "Currently"),
        ("finished","Finished"),
        ("canceled", "Canceled")
    )
    status = models.CharField(max_length=20, choices=BOOTCAMP_STATUS_CHOICES, default="draft")
    instructor = models.ManyToManyField(to=CustomUser, related_name="teachers")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_online = models.BooleanField(default=True)
    title = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(to=BootcampCategory, on_delete=models.CASCADE, null=True ,related_name="bootcamp_list")
    capacity = models.PositiveIntegerField()
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    hours = models.CharField(max_length=50)
    days = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)



    def __str__(self):
        return self.title
    






class BootcampRegistration(models.Model):
    volunteer = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    bootcamp = models.ForeignKey(to=Bootcamp, on_delete=models.CASCADE, related_name="registrations")

    PAYMENT_STATUS_CHOICES = (
        ("installment_pay", "Installment_Pay"),
        ("check", "Check"),
        ("safte", "Safte"),
    )
    payment_type = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default="check")
    installment_count = models.PositiveIntegerField(null=True, blank=True)

    def clean(self):
        super().clean()
        if self.payment_type == "installment_pay" and not self.installment_count:
            raise ValidationError("Users must mentaion the count of the installment pay!")

    registered_at = models.DateTimeField(auto_now_add=True)


    REGISTRATION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewing', 'Reviewing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS_CHOICES, default="pending")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(to=CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_enrollments')
    comment = models.TextField(null=True, blank=True)
    phone_number = PhoneNumberField(region='IR', unique=True)
    slug = models.SlugField(unique=True)
    admin_status_comment = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.status
    




class SMSLog(models.Model):
    phone_number = models.CharField(max_length=20)
    full_name = models.CharField(max_length=180)
    STATUS_SMS = (
        ("success", "Success"),
        ("unsuccess", "Unsuccess")
    )

    status = models.CharField(max_length=100, choices=STATUS_SMS)
    response_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"SMS to {self.phone_number} - {self.status}"





class ClassNotifications(models.Model):
    title = models.CharField(max_length=100)
    bootcampRegistration = models.ForeignKey(to=BootcampRegistration, on_delete=models.PROTECT, null=True, blank=True)
    admin_message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('sent', 'Sent')], default='pending')
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.title