from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from account.permissions import GroupPermission, GroupHasDynamicPermission, create_permission_class
from rest_framework.views import APIView
from .serializers import BlogCategorySerializer, UploadBlogSerializer, BlogSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from account.utils.logging import log_admin_activity
from django.http import FileResponse
from rest_framework.response import Response
from .models import CategoryBlog, Blog
from django.db import transaction
from account.views import CustomPagination
from .filters import CategoryBlogFilter






#test passed
#اضافه کردن دسته بندی توسط سوپریوزر و پنل ادمین
class AddCategoryBlogView(CreateAPIView):
    queryset = CategoryBlog.objects.all()
    permission_classes = [IsAuthenticated, create_permission_class(["blog.add_categoryblog"])]
    serializer_class = BlogCategorySerializer
    def perform_create(self, serializer):
        with transaction.atomic():
            category = serializer.save()
            try:
                log_admin_activity(
                    request=self.request,
                    action="created category for blog",
                    instance=category.name
                )
            except Exception as e:
                pass    
        
        




#test passed
class UploadBlogView(CreateAPIView):
    """  ساختن وبلاگ توسط ادمین با دسترسی و ثبت لاگ برای رصد فعالیت های کاربر پنل """
    queryset = Blog.objects.all()
    serializer_class = UploadBlogSerializer
    permission_classes = [IsAuthenticated, create_permission_class(["blog.add_blog"])]
   

    def perform_create(self, serializer):
        with transaction.atomic():
            blog = serializer.save(uploaded_by=self.request.user)
            try:
                log_admin_activity(
                    request=self.request,
                    action="Uploaded a new blog",
                    instance=f"Title:{blog.title}, ID:{blog.id}"
                )
            except Exception:
                pass







#test passed
class DeleteCategoryBlogView(DestroyAPIView):
    queryset = CategoryBlog.objects.all()
    permission_classes = [IsAuthenticated, create_permission_class(["blog.delete_categoryblog"])]
    serializer_class = BlogCategorySerializer
    lookup_field = 'slug'
    def perform_destroy(self, instance):
        with transaction.atomic():
            category_name = instance.name 
            instance.delete()
            try:
                log_admin_activity(
                    request=self.request,
                    action="Deleted category blog",
                    instance=category_name
                )
            except Exception:
                pass




#test passed
class ListCateogryBlogView(ListAPIView):
    """لیست دسته بندی ها های وبلاگ ها"""
    queryset = CategoryBlog.objects.all().order_by("-date_created")
    permission_classes = [IsAuthenticated, create_permission_class(["blog.view_categoryblog"])]
    serializer_class = BlogCategorySerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    filterset_class = CategoryBlogFilter

    


#test passed
class EditBlogView(UpdateAPIView):
    serializer_class = UploadBlogSerializer
    permission_classes = [IsAuthenticated, create_permission_class(["blog.change_blog"])]
    queryset = Blog.objects.all()
    lookup_field = 'slug'
    def perform_update(self, serializer):
        with transaction.atomic():
            blog = serializer.save()
            try:
                log_admin_activity(
                    request=self.request,
                    action="edited blog",
                   instance=f"Title: {blog.title}, ID: {blog.id}"
                )
            except Exception:
                pass    


    




#test passed
class DeleteBlogView(DestroyAPIView):
    permission_classes = [IsAuthenticated, create_permission_class(["blog.delete_blog"])]
    serializer_class = UploadBlogSerializer
    queryset = Blog.objects.all()
    lookup_field = "slug"
    def perform_destroy(self, instance):
        with transaction.atomic():
            blog_name = instance.name 
            instance.delete()
            try:
                log_admin_activity(
                    request=self.request,
                    action="Deleted a blog",
                    instance=blog_name
                )
            except Exception:
                pass


    




#test passed
class DetailBlogView(RetrieveAPIView):
    queryset = Blog.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UploadBlogSerializer
    lookup_field = "slug"





#tets passed
class ListBlogView(ListAPIView):
    queryset = Blog.objects.filter(status="published").order_by("date_added")
    permission_classes = [AllowAny]
    serializer_class = BlogSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "status", "content"]
    filterset_fields = ["status", "date_added"]
    ordering_fields = ["date_added"]





#test passed
class AdminListBlogView(ListAPIView):
    queryset = Blog.objects.all().order_by("-date_added")
    permission_classes = [IsAuthenticated, create_permission_class(["blog.view_blog"])]
    serializer_class = BlogSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "status", "content"]
    filterset_fields = ["status", "date_added"]
    ordering_fields = ["-date_added"]





class BlogDownloadView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, slug, format=None):
        try:
            blog = Blog.objects.get(slug=slug)

            if blog.file and hasattr(blog.file, 'path'):
                file_path = blog.file.path
                response = FileResponse(open(file_path, 'rb'), as_attachment=True)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = f'attachment; filename="{blog.file.name}"'
                return response
            else:
                return Response({"detail": "No file available for this blog."}, status=404)

        except Blog.DoesNotExist:
            return Response({'detail': 'Blog not found.'}, status=404)
        except Exception as e:
            # اگر ارور دیگه‌ای پیش اومد، می‌تونی اینجا مدیریت کنی
            return Response({'detail': f'Error: {str(e)}'}, status=500)