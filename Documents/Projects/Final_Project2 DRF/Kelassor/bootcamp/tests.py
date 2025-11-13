from .models import Bootcamp, BootcampRegistration, BootcampCategory,ClassNotifications
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group 
from rest_framework.test import APITestCase
from django.utils.text import slugify
from account.models import CustomUser 
from datetime import date, timedelta ,datetime
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
import datetime
import uuid 



User = get_user_model()




class AdminCreateBootcampViewTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username="admin@%1", email="admintest1@email.com",
        national_id="8976756453", phone="+989966955432", slug="admin-test")

        self.regular_user = User.objects.create_user(username="user@%1", email="usertest1@email.com",
        national_id="8976758453", phone="+989966955433", slug="user-test")

        self.instructor1 = User.objects.create_user(username="teacher@%1", email="teachertest1@email.com",
        national_id="8976758653", phone="+989966951433", slug="teacher-test", last_name="testteacher")

        
        support_group = Group.objects.create(name="SupportPanel")
        self.admin_user.groups.add(support_group)
        self.admin_user.is_superuser = True
        self.admin_user.save()

        self.category = BootcampCategory.objects.create(name="AI Bootcamp", slug="ai")

        self.url = reverse("create-bootcamp-by-admin")


        self.payload = {
            "instructor": ["Instructor1"],  # چون slug_field='last_name' هست
            "title": "AI Bootcamp",
            "price": 1000,
            "capacity": 25,
            "category": self.category.pk,  # فیلد category دیگه url نیست پس pk بفرست
            "description": "Test bootcamp description",
            "start_date": "2025-06-01",
            "end_date": "2025-06-20",
            "hours": 40,
            "days": 10,
        }

    def get_token(self, user):
        return str(RefreshToken.for_user(user).access_token)
        


    def test_create_bootcamp_without_permission(self):
        token = self.get_token(self.regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





class DetailBootCampViewTest(APITestCase):
    def setUp(self):
        self.category = BootcampCategory.objects.create(name="AI", slug="ai")
        self.bootcamp = Bootcamp.objects.create(
            title="AI Beginner",
            price=500,
            capacity=20,
            category=self.category,
            description="Desc",
            start_date=datetime.date(2025, 1, 1),
            end_date=datetime.date(2025, 2, 1),
            hours=40,
            days=20,
            slug="ai-beginner",
            status="registering",
            is_online=True,
        )
        self.url = reverse('detail-bootcamp', kwargs={'slug': self.bootcamp.slug})

    def test_get_existing_bootcamp(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.bootcamp.slug)

    def test_get_nonexistent_bootcamp_returns_404(self):
        url = reverse('detail-bootcamp', kwargs={'slug': 'non-existent-slug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Bootcamp nor found !")

    def test_get_bootcamp_with_wrong_status_returns_404(self):
        self.bootcamp.status = "closed"
        self.bootcamp.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Bootcamp nor found !")







class ListBootCampRegistrationViewTest(APITestCase):
    def setUp(self):
        # گروه‌ها و کاربران
        self.group = Group.objects.create(name="SupportPanel")
        self.superuser = CustomUser.objects.create_user(username="admin@33", email="adminuser6@email.com",
        is_superuser=True, national_id="8767879875", phone="+989122343221")
        self.superuser.groups.add(self.group)

        self.user = CustomUser.objects.create_user(username="usernorm@33", email="normuser6@email.com",
        national_id="8761879875", phone="+989122313221")
        self.category=BootcampCategory.objects.create(name="testcat", slug="test-slug")

        # توکن JWT برای سوپر یوزر
        refresh = RefreshToken.for_user(self.superuser)
        self.token = str(refresh.access_token)
        self.bootcamp = Bootcamp.objects.create(
        title="Sample Bootcamp",
        price=100,
        capacity=10,
        category=self.category,  # حتما باید این رو داشته باشی
        description="Test bootcamp",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 2, 1),
        hours=40,
        days=20,
        slug="sample-bootcamp",
        status="registering",
        is_online=True,
    )    

        # نمونه بوتکمپ رجیستر (status pending و غیر pending)
        self.pending_registration = BootcampRegistration.objects.create(
            phone_number="1234567890",
            bootcamp=self.bootcamp,
            volunteer=self.user,
            comment="Pending user",
            payment_type="online",
            status="pending",
            reviewed_by=self.superuser,
            slug="test-bootcamp-registraion12"
        )
        self.approved_registration = BootcampRegistration.objects.create(
            phone_number="0987654321",
            comment="Approved user",
            bootcamp=self.bootcamp,
            volunteer=self.user,
            payment_type="offline",
            status="approved",
            reviewed_by=self.superuser,
            slug="test-bootcamp-registraion"
        )

        self.url = reverse('list-boortcamp-regitration')  # اسم روت رو متناسب با پروژه تغییر بده

    def test_access_without_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_without_permission(self):
        # لاگین با یوزر عادی بدون گروه
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_token(self.user)}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_with_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_status_pending(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.url, {'status': 'pending'})
        data = response.json()
        self.assertTrue(all(reg['status'] == 'pending' for reg in data['results']))

    def test_search_phone_number(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.url, {'search': '1234'})
        data = response.json()
        self.assertTrue(any('1234' in reg['phone_number'] for reg in data['results']))

    def test_ordering_registered_at(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.url, {'ordering': '-registered_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    







class CheckRegistrationStatusViewTest(APITestCase):
    def setUp(self):
        # ساخت گروه و کاربر سوپر یوزر
        self.group = Group.objects.create(name="SupportPanel")
        self.superuser = CustomUser.objects.create_user(username="admin@35", email="adminuser8@email.com",
        is_superuser=True, national_id="8767179875", phone="+989122743221")
        self.superuser.groups.add(self.group)

        self.user = CustomUser.objects.create_user(username="normaluser", email="normaluser8@email.com"
        ,national_id="8167179875", phone="+989122743229"                                          )

        # بوتکمپ و ثبت نام
        self.bootcamp = Bootcamp.objects.create(
            title="Test Bootcamp",
            price=100,
            capacity=10,
            category=BootcampCategory.objects.create(name="Cat", slug="cat"),
            description="desc",
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            hours=10,
            days=5,
            slug="test-bootcamp",
            status="registering",
            is_online=True,
        )

        self.registration = BootcampRegistration.objects.create(
            slug="test-registration",
            bootcamp=self.bootcamp,
            volunteer=self.user,
            phone_number="123456789",
            payment_type="online",
            status="pending",
        )

        # توکن سوپر یوزر
        refresh = RefreshToken.for_user(self.superuser)
        self.token = str(refresh.access_token)
        self.url = reverse('check-status-registrations', kwargs={'slug': self.registration.slug})

    def test_update_status_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            "status": "approved",
            "admin_status_comment": "Looks good"
        }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.registration.refresh_from_db()
        self.assertEqual(self.registration.status, "approved")
        self.assertEqual(self.registration.admin_status_comment, "Looks good")
        self.assertEqual(self.registration.reviewed_by, self.superuser)
        self.assertIsNotNone(self.registration.reviewed_at)

    def test_update_with_extra_fields_fails(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            "status": "approved",
            "admin_status_comment": "Looks good",
            "extra_field": "not allowed"
        }
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("extra_field", str(response.data))

    def test_update_without_permission_fails(self):
        # لاگین با کاربر عادی بدون گروه SupportPanel
        normal_refresh = RefreshToken.for_user(self.user)
        normal_token = str(normal_refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {normal_token}')
        data = {
            "status": "approved",
            "admin_status_comment": "Looks good"
        }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)






class MassNotificationViewTest(APITestCase):
    def setUp(self):
        # کاربر با گروه های لازم
        self.user = CustomUser.objects.create_user(username="admin#$", email="adminuser@email.com",
        national_id="9865123281", phone="+989356542131", slug="admin-testuser1")
        self.user.groups.add(Group.objects.get_or_create(name="SuperUser")[0])

        # توکن JWT
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.url = reverse('create-notify-by-admin')  # فرض بر این که آدرس url را درست تنظیم کردی

        self.valid_data = {
            "title": "Important Update",
            "message": "This is a test notification",
            "recipients": [self.user.id],  # یا هر شناسه‌ای که تو serializer نیاز داری
        }

    # def test_create_notifications_success(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    #     response = self.client.post(self.url, self.valid_data, format='json')
    #     self.assertEqual(response.status_code, 201)
    #     self.assertIn("create-notify-by-admin", response.data["detail"])

    def test_create_notifications_without_auth(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertIn(response.status_code, [401, 403])

    def test_create_notifications_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        invalid_data = {
            "title": "",  # فرض کنیم عنوان نباید خالی باشه
            "message": "This is a test notification",
            "recipients": []
        }
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, 400)

