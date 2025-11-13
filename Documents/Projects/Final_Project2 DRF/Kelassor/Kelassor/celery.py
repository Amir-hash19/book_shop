from celery import Celery 
import os




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kelassor.settings')

app = Celery('Kelassor')

# تنظیمات celery رو از settings.py بارگذاری کن با پیشوند CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# پیدا کردن taskهای ثبت‌شده در اپ‌ها
app.autodiscover_tasks()

