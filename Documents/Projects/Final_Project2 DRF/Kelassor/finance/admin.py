from django.contrib import admin
from .models import Invoice, Payment ,Transaction




@admin.register(Invoice)
class AdminInvoice(admin.ModelAdmin):
    list_display = ("client", "amount", "deadline", "created_at")
    search_fields = ("client", "description", "amount")
    list_filter = ("is_paid", "deadline")
    ordering = ("-created_at", )
    list_per_page = 20




@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    list_display = ("user", "method", "amount", "paid_at", "tracking_code")
    search_fields = ("user", "amount", "paid_at")
    list_filter = ("paid_at", "method", "is_verified")
    list_per_page = 20
    ordering = ("-paid_at", "is_verified")




@admin.register(Transaction)
class AdminTransaction(admin.ModelAdmin):
    list_display = ("user", "amount", "is_verified")
    search_fields = ("description", "user", "amount")
    list_filter = ("transaction_date", "is_verified")
    ordering = ("-transaction_date", )
    list_per_page = 40
