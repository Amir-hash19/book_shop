from django.contrib import admin
from .models import Blog, CategoryBlog



@admin.register(CategoryBlog)
class CategoryBlogAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "date_created")
    list_editable = ("slug", )
    list_filter = ("date_created", )
    search_fields = ("name", )
    list_per_page = 10


@admin.register(Blog)
class AdminBlog(admin.ModelAdmin):
    list_display = ("title", "date_added", "status")
    list_editable = ("status", )
    search_fields = ("title", "slug", "content")
    # list_display_links = ("title", "status")
    list_filter = ("status", "date_added")
    ordering = ("-date_added", )
    list_per_page = 30
    fields = (("title", "status", "slug"), "content", "blogcategory", "file", "uploaded_by")
