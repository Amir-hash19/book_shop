from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UploadBlogSerializer
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from .models import Blog, CategoryBlog
from .views import UploadBlogView
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta
import io

User = get_user_model()


class UploadBlogViewTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory() 
       


        self.support_group=Group.objects.create(name="SupportPanel")
        self.superuser_group=Group.objects.create(name="SuperUser")


        self.user_with_permission = User.objects.create_user(username="permitted@12",
        password="pass1234", phone="+989917652134", email="permitted12@email.com", national_id="4444444444")
        self.user_with_permission.groups.add(self.support_group, self.superuser_group)



        self.user_without_permission = User.objects.create_user(username="noperm@12",
        password="pass1234", phone="+989213412564", email="noperm12@email.com", national_id="7685940328")

        self.category=CategoryBlog.objects.create(name="tech")

        
        self.valid_data = {
            "title":"test blog",
            "content":"this is test blog content",
            "blogcategory":self.category.id
        }

        self.data = self.valid_data
        self.url=reverse("create-blog")

    def test_upload_blog_with_force_authenticate(self):
        request = self.factory.post("/api/blogs/", self.data, format='json')
        force_authenticate(request, user=self.user_with_permission)
        view = UploadBlogView.as_view()


        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.first().uploaded_by, self.user_with_permission)








class ListCategoryBlogViewTest(APITestCase):
    def setUp(self):
        self.support_group = Group.objects.create(name="SupportPanel")
        self.superuser_group = Group.objects.create(name="SuperUser")

        self.permitted_user = User.objects.create_user(
            username="allowed@12",
            password="123456$@",
            email="allowed#12@email.com",
            national_id="8765434567",
            phone="+989356732134"
        )
        self.permitted_user.groups.add(self.support_group, self.superuser_group)

        self.unauthorized_user = User.objects.create_user(
            username="notallowed@12",
            password="123456",
            email="allowed#14@email.com",
            national_id="8765434568",
            phone="+989356732131"
        )

        self.category1 = CategoryBlog.objects.create(name="Tech", date_created=datetime.now())
        self.category2 = CategoryBlog.objects.create(name="Business", date_created=datetime.now() - timedelta(days=1))

        self.url = reverse("list-category-blog")




    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)





    def test_list_categories_by_permitted_user(self):
        token = self.get_token_for_user(self.permitted_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)




    def test_unauthenticated_user_cannot_access(self):
        self.client.credentials()  # پاک کردن هر نوع توکن قبلی
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




    def test_user_without_permission_cannot_access(self):
        token = self.get_token_for_user(self.unauthorized_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_search_category_by_name(self):
        token = self.get_token_for_user(self.permitted_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url, {'search': 'Tech'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Tech")



    def test_pagination_works(self):
        token = self.get_token_for_user(self.permitted_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        for i in range(15):
            CategoryBlog.objects.create(name=f"Extra {i}", date_created=datetime.now())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 20)  # در صورت داشتن pagination 10تایی







class DeleteBlogViewTest(APITestCase):
    def setUp(self):
        # ایجاد گروه‌ها
        self.support_group = Group.objects.create(name="SupportPanel")
        self.superuser_group = Group.objects.create(name="SuperUser")

        # ایجاد کاربران
        self.user_with_permission = User.objects.create_user(username="alloweduser@12",
        password="pass1234#$", email="alloweduser@email.com", national_id="4329875601", phone="+989944321259")
        self.user_with_permission.groups.add(self.support_group, self.superuser_group)

        self.user_without_permission = User.objects.create_user(username="notalloweduser@12",
        password="pass1234#$", email="notalloweduser@email.com", national_id="4329874601", phone="+989944321269")

        # دسته‌بندی بلاگ برای استفاده
        self.category = CategoryBlog.objects.create(name="Tech")

        # بلاگی که متعلق به user_with_permission است
        self.blog_owned = Blog.objects.create(
            title="User Blog",
            content="Content",
            blogcategory=self.category,
            uploaded_by=self.user_with_permission
        )

        # بلاگی که متعلق به user_without_permission نیست
        self.blog_other = Blog.objects.create(
            title="Other Blog",
            content="Other Content",
            blogcategory=self.category,
            uploaded_by=self.user_without_permission
        )

        self.url = lambda slug: reverse("delete-blog", kwargs={"slug": slug})  # فرض بر این است نام url به این شکل است

        # کلاینت و توکن کاربر دارای دسترسی
        self.client = APIClient()
        self.token = self.get_token_for_user(self.user_with_permission)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_delete_own_blog_success(self):
        response = self.client.delete(self.url(self.blog_owned.slug))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Blog.objects.filter(pk=self.blog_owned.pk).exists())

    def test_cannot_delete_other_user_blog(self):
        response = self.client.delete(self.url(self.blog_other.pk))
        self.assertEqual(response.status_code, 404)  # چون در queryset فیلتر شده و بلاگ پیدا نمیشه

    def test_unauthenticated_cannot_delete(self):
        self.client.credentials()  # حذف توکن برای شبیه سازی غیرمجاز بودن
        response = self.client.delete(self.url(self.blog_owned.pk))
        self.assertEqual(response.status_code, 401)

    def test_user_without_permission_cannot_delete(self):
        # ست کردن توکن کاربر بدون دسترسی
        token = self.get_token_for_user(self.user_without_permission)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.delete(self.url(self.blog_owned.pk))
        self.assertEqual(response.status_code, 403)





class BlogDownloadViewTest(APITestCase):
    def setUp(self):
        # ایجاد گروه و کاربر
        self.support_group = Group.objects.create(name="SupportPanel")
        self.user = User.objects.create_user(username="user1", password="pass1234@$",
        email="user1@email.com", national_id="8769587342", phone="+989123456121"                                     )
        self.user.groups.add(self.support_group)

        # ایجاد دسته‌بندی
        self.category = CategoryBlog.objects.create(name="Tech")

        # ایجاد فایل تستی
        self.test_file = SimpleUploadedFile("testfile.txt", b"Hello World", content_type="text/plain")

        # ایجاد بلاگ با فایل
        self.blog_with_file = Blog.objects.create(
            title="Blog with File",
            content="Content",
            blogcategory=self.category,
            uploaded_by=self.user,
            file=self.test_file,
            slug="blog-with-file"
        )

        # ایجاد بلاگ بدون فایل
        self.blog_without_file = Blog.objects.create(
            title="Blog without File",
            content="Content",
            blogcategory=self.category,
            uploaded_by=self.user,
            slug="blog-without-file"
        )

        self.url = lambda slug: reverse("blog-download", kwargs={"slug": slug})

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_download_blog_file_success(self):
        response = self.client.get(self.url(self.blog_with_file.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/octet-stream')
        self.assertIn('attachment; filename="', response['Content-Disposition'])

    def test_download_blog_no_file(self):
        response = self.client.get(self.url(self.blog_without_file.slug))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "No file available for this blog.")

    def test_blog_not_found(self):
        response = self.client.get(self.url("non-existent-slug"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Blog not found.")



