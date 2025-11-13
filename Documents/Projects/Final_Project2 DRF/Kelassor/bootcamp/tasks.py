from celery import shared_task
from django.conf import settings
from celery.exceptions import Retry
import time
from kavenegar import KavenegarAPI, APIException, HTTPException
from .models import SMSLog, ClassNotifications

api = KavenegarAPI(settings.KAVENEGAR_API_KEY)







@shared_task(bind=True, max_retries=3, default_retry_delay=5, ignore_result=True)
def send_sms_to_user(self, phone, full_name):#ارسال پیام به یوزر که ایا درخواستش قبول شده یا نه 
    try:
        message = f"{full_name} The result of your registration just came! check website please !"
        params = {
            "receptor":phone,
            "message":message,
            "sender":"2000660110"
        }
        response = api.sms_send(params)

        SMSLog.objects.create(
            phone_number = phone,
            full_name = full_name,
            status = "Success",
            response_message = str(response)
        )
        return response
    
    except (APIException ,HTTPException) as e:
        SMSLog.objects.create(
            phone_number = phone,
            full_name = full_name,
            status = "Unsuccess",
            response_message = str(e)
        )
        try:
            self.retry(exc=e) 
        except Retry:
            return {"status":"failed", "reason":str(e)}    
        




@shared_task(bind=True, max_retries=4, default_retry_delay=60)
def send_sms_notification(notification_id):
    try:
        notification = ClassNotifications.objects.get(id=notification_id)
        phone_number = notification.bootcampRegistration.phone_number.as_e164
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        api.sms_send({
            'receptor': phone_number,
            'message': notification.admin_message
        })
        notification.status = 'sent'
        notification.save()
    except APIException as e:
        notification.status = 'failed'
        notification.save()
    except ClassNotifications.DoesNotExist:
        pass  # اگر نوتیفیکیشن پیدا نشد، نادیده بگیر




