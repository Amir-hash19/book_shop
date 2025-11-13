from django.contrib import admin
from. models import Ticket, TicketMessage




# admin.site.register(TicketMessage)




@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    list_display = ("title", "user", "bootcamp", "status", "created_at")
    search_fields = ("title", "description", "user", "slug")
    list_filter = ("status", "created_at")
    ordering = ("-created_at", )
    list_per_page = 30



@admin.register(TicketMessage)
class AdminTicketMessage(admin.ModelAdmin):
    list_display = ("sender", "message_status", "created_at", "title")
    search_fields = ("title", "created_at", "slug", "message")
    list_filter = ("created_at", "message_status", "admin")
    list_per_page = 30
    ordering = ("-created_at", )


