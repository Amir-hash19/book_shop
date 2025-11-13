from django.db.models.signals import post_save, m2m_changed, pre_save
from django.utils.timezone import now
from .permissions import is_supportpanel_user
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import CustomUser
from .tasks import send_welcome_sms_task
from django.utils.text import slugify
from datetime import datetime
import uuid

User = get_user_model()

@receiver(post_save, sender=CustomUser)
def send_welcome_message(sender, created, instance, **kwargs):
    if created:
        last_name = instance.last_name
        user_phone_number = str(instance.phone)

        
        send_welcome_sms_task.delay(last_name, user_phone_number)
        



@receiver(pre_save, sender=CustomUser)
def generate_slug_customeuser(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.username)
        unique_suffix = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"{base_slug}-{unique_suffix}")






@receiver(m2m_changed, sender=User.groups.through)
def update_user_flags_on_group_change(sender, instance, action, pk_set, **kwargs):
    support_group = Group.objects.filter(name="SupportPanel").first()
    super_group = Group.objects.filter(name="SuperUser").first()


    if action == "post_add":
        if support_group and support_group.pk in pk_set:
            instance.is_staff = True
            instance.save()

        if super_group and super_group.pk in pk_set:
            instance.is_superuser = True
            instance.save()        



    elif action == "post_remove":
        user_groups = instance.groups.all()

        if super_group and support_group not in user_groups:
            instance.is_staff = False
            instance.save()

        if super_group and super_group not in user_groups:
            instance.is_superuser = False
            instance.save()
                         