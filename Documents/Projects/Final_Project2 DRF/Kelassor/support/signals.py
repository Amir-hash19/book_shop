from django.db.models.signals import pre_save
from .models import Ticket, TicketMessage
from django.utils.text import slugify
from django.dispatch import receiver
from .models import Ticket, TicketMessage
from datetime import datetime
import uuid



@receiver(pre_save, sender=Ticket)
def generate_ticket_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        unique_suffix = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"-{base_slug}-{unique_suffix}")





@receiver(pre_save, sender=TicketMessage)
def generate_ticket_message_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        unique_suffix = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"-{base_slug}-{unique_suffix}")





