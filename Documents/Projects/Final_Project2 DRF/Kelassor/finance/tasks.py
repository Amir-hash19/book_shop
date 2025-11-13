from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from kavenegar import KavenegarAPI
from .models import Invoice
import os

api = KavenegarAPI(settings.KAVENEGAR_API_KEY)




@shared_task(bind=True, max_retries=3, default_retry_delay=60, ignore_result=True)  
def send_sms_for_invoice_task(self, phone_client, last_name):
    api_key = os.getenv('KAVENEGAR_API_KEY')  
    client = KavenegarAPI(api_key)
    cache_key = f"welcome_sms:{phone_client}"
    message = f"This message from kelassor, new invoice created for you please check your panel-->'https://kelaasor.com/'<--"

    try:
        params = {
            "receptor":phone_client,
            "sender":"2000660110",
            "message":message
        }
        response = client.sms_send(params)  
        return response
    except Exception as e:
        raise self.retry(exc=e)
    finally:
        cache.delete(cache_key)
    



@shared_task(bind=True, max_retries=3, default_retry_delay=5, ignore_result=True)
def notify_when_deadline(self, phone, name):
    from django.utils.timezone import localdate
    today = localdate()
    
    invoices = Invoice.objects.filter(is_paid=False, deadline__lt=today)
    
    for invoice in invoices:
        user = invoice.client
        phone = str(user.phone) 
        name = invoice.client.get_full_name()
        
        message = f"Dear {name}, Amount: {invoice.amount} please check your panel"    
        
        params = {
            "receptor":phone,
            "message":message,
            "sender":"2000660110"
        }
        try:
            response = api.sms_send(params)
            if response.get('status') != 200:
                raise Exception("SMS sending failed.")
        except Exception as e:
            raise self.retry(exc=e)    
    return f"SMS notifications sent successfully"
