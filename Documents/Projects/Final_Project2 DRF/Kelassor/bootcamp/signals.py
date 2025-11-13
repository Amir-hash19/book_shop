from django.db.models.signals import post_save, pre_save
from .models import BootcampRegistration, Bootcamp, BootcampCategory
from django.dispatch import receiver
from django.utils.text import slugify
from .tasks import send_sms_to_user
from django.core.exceptions import ValidationError
from django.db.models import F
from django.db import transaction
from datetime import datetime
import uuid




@receiver(pre_save, sender=Bootcamp)
def generate_slug_bootcamp(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        unique_suffix = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"{base_slug}-{unique_suffix}")




@receiver(pre_save, sender=BootcampRegistration)
def generate_slug_registration(sender, instance, **kwargs):
    if not instance.slug:
        date_part = datetime.now().strftime("%Y%m%d")
        uuid_part = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"b-registration-{date_part}-{uuid_part}")




@receiver(pre_save, sender=BootcampCategory)
def generate_slug_category(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.name)
        unique_suffix = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"{base_slug}-{unique_suffix}")




@receiver(post_save, sender=BootcampRegistration)
def check_capacity_bootcamp(sender, instance, created, **kwargs):
    if not created and instance.status == "approved":
        bootcamp = instance.bootcamp
        with transaction.atomic():
            updated = Bootcamp.objects.filter(id=bootcamp.id, capacity__gt=0).update(capacity=F("capacity")-1)
            if not updated:
                raise ValidationError(f"bootcamp {bootcamp.title} is full")




@receiver(pre_save, sender=BootcampRegistration)
def notify_user(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = BootcampRegistration.objects.get(id=instance.pk)
        except BootcampRegistration.DoesNotExist:
            previous = None    

        if previous and previous.status != instance.status:
            phone = str(instance.phone_number)
            full_name = str(instance.volunteer)

            send_sms_to_user.delay(phone, full_name)





