from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (AddCategoryBlogView, UploadBlogView, DeleteCategoryBlogView, 
                    ListCateogryBlogView, EditBlogView, DeleteBlogView, DetailBlogView, 
                    ListBlogView, AdminListBlogView, BlogDownloadView)



urlpatterns = [
    path("add-category/", AddCategoryBlogView.as_view(), name="create-category-blog"),
    path("upload-blog/", UploadBlogView.as_view(), name="create-blog"),
    path("delete-category/<slug:slug>/", DeleteCategoryBlogView.as_view(), name="delete-category-blog"),
    path("list-category-blogs/", ListCateogryBlogView.as_view(), name="list-category-blog"),
    path("edit-blog/<slug:slug>/", EditBlogView.as_view(), name="edit-blog-adminsupport"),
    path("delete-blog/<slug:slug>/", DeleteBlogView.as_view(), name="delete-blog"),
    path("detail-blog/<slug:slug>/", DetailBlogView.as_view(), name="detail-blog"),
    path("list-blog/", ListBlogView.as_view(), name="list-blogs"),
    path("list-all-blogs/", AdminListBlogView.as_view(), name="list-all-blogs-admin"),
    path('blog/download/<slug:slug>/', BlogDownloadView.as_view(), name='blog-download'),




    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
