from celery.exceptions import MaxRetriesExceededError 
from kavenegar import KavenegarAPI, APIException 
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
from .models import CustomUser
from celery import shared_task
import random 
import redis
import os



api = KavenegarAPI(settings.KAVENEGAR_API_KEY)

@shared_task(bind=True, max_retries=3, default_retry_delay=60, ignore_result=True)  
def send_welcome_sms_task(self, user_phone_number, last_name):
    api_key = os.getenv('KAVENEGAR_API_KEY')  
    client = KavenegarAPI(api_key)
    cache_key = f"welcome_sms:{user_phone_number}"

    try:
        params = {
            'receptor': user_phone_number,  
            'message': f"Welcome and tnx for SigningUp {last_name}",  
            'sender': "2000660110",  
        }
        response = client.sms_send(params)  
        return response
    except Exception as e:
        raise self.retry(exc=e)
    finally:
        cache.delete(cache_key)








@shared_task(bind=True, max_retries=5, default_retry_delay=60, ignore_result=True) 
def send_otp_task(self, phone):
    otp = str(random.randint(100000, 999999))
    cache.set(f"otp:{phone}", otp, timeout=180)
    cache_key = f"otp{phone}"


    try:
        params = {
            "sender": "2000660110",
            "receptor":phone,
            "message":f"Your OTP code is: {otp}"
        }
        response = api.sms_send(params)
        print(f"OTP for {phone}: {otp}, SMS sent successfully, this is only credit for 2minutes!")
        return otp
    except Exception as e:
        raise self.retry(exc=e)
    finally:
        cache.delete(cache_key)








@shared_task(bind=True,  max_retries=4, default_retry_delay=60, ignore_result=True)
def send_birthday_sms(self):
    today = timezone.now().date()
    users = CustomUser.objects.filter(birthday__month=today.month, birthday__day=today.day)
    
    api_key = os.getenv('KAVENEGAR_API_KEY') 

    for user in users:
        try:
            api.sms_send({
                "receptor":user.phone,
                "message":f"{user.first_name} Happy Birthday all the best for you",
                "sender":"2000660110",
            })
        except APIException as e:
            print(f"Error sending to {user.phone}: {str(e)}")    
            try:
                self.retry(exc=e)
            except MaxRetriesExceededError:
                print(f"[Retry Failed] Could not send to {user.phone} after max retries.")


                