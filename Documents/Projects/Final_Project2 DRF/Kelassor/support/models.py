from django.db import models
from account.models import CustomUser
from bootcamp.models import Bootcamp
from phonenumber_field.modelfields import PhoneNumberField




class Ticket(models.Model):
    TICKET_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("answered", "Answered"),
        ("notanswered", "NotAnswered"),
        ("closed", "Closed")
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="ticket_owner", null=True)
    bootcamp = models.ForeignKey(to=Bootcamp, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default="pending")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    





class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True,related_name='messages')
    sender = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=True, blank=True,related_name="customer_sender")
    user_phone = PhoneNumberField(unique=True, region='IR', null=True, blank=True)
    MESSAGE_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("answered", "Answered"),
        ("notanswered", "NotAnswered"),
        ("closed", "Closed")
    )

    message_status = models.CharField(max_length=20, choices=MESSAGE_STATUS_CHOICES, default="pending")
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='ticket_attachments/', null=True, blank=True)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    admin = models.ForeignKey(to=CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    admin_response = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return self.title
    





