from django.db.models.signals import pre_save
from .models import Blog, CategoryBlog
from django.utils.text import slugify
from django.dispatch import receiver
from .models import Blog, CategoryBlog
import uuid



@receiver(pre_save, sender=Blog)
def generate_blog_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        unique_suffix = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"{base_slug}-{unique_suffix}")





@receiver(pre_save, sender=CategoryBlog)
def generate_category_blog_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.slug)
        unique_suffix = str(uuid.uuid4())[:8]
        instance.slug = slugify(f"{base_slug}-{unique_suffix}")