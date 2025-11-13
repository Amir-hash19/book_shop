from django.contrib import admin
from .models import *



@admin.register(BootcampCategory)
class AdminBootcampCategory(admin.ModelAdmin):
    list_display = ("name", "date_created", "slug")
    search_fields = ("name", )
    list_filter = ("date_created", )
    ordering = ("-date_created", )
    list_per_page = 20





@admin.register(Bootcamp)
class AdminBootcamp(admin.ModelAdmin):
    list_display = ("title", "created_at", "status", "is_online")
    search_fields = ("title", "description", "days")
    list_filter = ("status", "created_at", "hours", "days", "is_online")
    ordering = ("-created_at", "is_online")
    list_per_page = 30
    fields = (("title", "is_online", "hours", "days"), "description", "capacity", "start_date", "end_date", "price", "slug", "category", "status", "instructor")





@admin.register(BootcampRegistration)
class AdminBootcampRegistration(admin.ModelAdmin):
    list_display = ("volunteer", "bootcamp", "status", "registered_at")
    search_fields = ("status", "comment", "payment_type", "bootcamp")
    list_filter = ("status", "payment_type", "installment_count", "volunteer")
    ordering = ("-registered_at", )
    list_per_page = 20
    fields = (("bootcamp", "slug", "volunteer","status", "payment_type", "installment_count", "phone_number"), "comment", "reviewed_at", "reviewed_by", "admin_status_comment")




@admin.register(SMSLog)
class AdminSMSLog(admin.ModelAdmin):
    list_display = ("full_name", "phone_number", "status")
    list_filter = ("status", "created_at")
    ordering = ("-created_at", )
    list_per_page = 40
    search_fields = ("response_message", "full_name")






@admin.register(ClassNotifications)
class AdminClassNotifications(admin.ModelAdmin):
    list_display = ("title", "sent_at", "status")
    search_fields = ("title", "admin_message")
    list_filter = ("status", "sent_at")
    list_per_page = 10
    ordering = ("-sent_at", )

