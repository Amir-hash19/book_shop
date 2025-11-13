from django.db.models.signals import pre_save, post_save
from rest_framework.exceptions import ValidationError
from .models import Invoice, Payment, Transaction
from .tasks import send_sms_for_invoice_task
from django.utils.text import slugify
from django.dispatch import receiver
from datetime import datetime
import uuid




@receiver(pre_save, sender=Invoice)
def generate_invoice_slug(sender, instance, **kwargs):
    if not instance.slug:
        date_part = datetime.now().strftime('%Y%m%d')
        uuid_part = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"invoice-{date_part}-{uuid_part}")




@receiver(pre_save, sender=Payment)
def generate_invoice_slug(sender, instance, **kwargs):
    if not instance.slug:
        date_part = datetime.now().strftime("%Y%m%d")
        uuid_part = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"payment-{date_part}-{uuid_part}")




@receiver(pre_save, sender=Transaction)
def generate_transaction_slug(sender, instance, **kwargs):
    if not instance.slug:
        date_part = datetime.now().strftime("%Y%m%d")
        uuid_part = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"transaction-{date_part}-{uuid_part}")




@receiver(post_save, sender=Payment)
def create_transaction_for_payment(sender, created, instance, **kwargs):
    if created:
        try:
            Transaction.objects.create(
                user=instance.user,
                amount=instance.amount,
                description=f"Payment for invoice {instance.invoice.created_at}",
                transaction_type='debit'
            )
        except Exception as e:
            raise ValidationError(f"Error craeting transaction{str(e)}")
            




@receiver(post_save, sender=Invoice)
def call_client_for_invoice(created, sender, instance, **kwargs):
    if created:
        phone_client = str(instance.client.phone)
        last_name = instance.client.last_name
        
        send_sms_for_invoice_task.delay(phone_client, last_name)

