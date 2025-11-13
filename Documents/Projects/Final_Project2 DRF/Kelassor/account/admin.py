from django.contrib import admin
from .models import CustomUser, AdminActivityLog


@admin.register(CustomUser)
class CustomeUserAdmin(admin.ModelAdmin):
    list_display = ("username", "last_name", "date_joined", "email")
    list_filter = ("gender", "date_joined")
    ordering = ("-date_joined", )
    search_fields = ("username", "email", "phone")
    list_per_page = 20
    fields = (("first_name", "last_name", "email", "phone" , "username", "slug"),
            "about_me", "national_id", "birthday", "password", "gender", "is_staff", "is_active", "is_superuser" , "groups")


admin.site.register(AdminActivityLog)
    