from django.utils.timezone import now
from account.models import AdminActivityLog

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # اگر چند IP ارسال شده بود، اولین IP واقعی رو برمی‌گردونه
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

def log_admin_activity(request, action, instance=None):
    user = request.user
    if not user.is_authenticated:
        return

    # فقط اگر کاربر عضو گروه supportpanel بود لاگ ثبت می‌کنه
    if not user.groups.filter(name="SupportPanel").exists():
        return

    ip = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "unknown")
    timestamp = now().strftime("%Y-%m-%d %H:%M")

    detail = f'User "{user.username}" {action}'
    if instance:
        detail += f' "{instance}"'
    detail += f' at {timestamp} from IP {ip}'

    AdminActivityLog.objects.create(
        admin_user=user,
        action=action,
        detail=detail,
        ip_address=ip,
        user_agent=user_agent
    )
