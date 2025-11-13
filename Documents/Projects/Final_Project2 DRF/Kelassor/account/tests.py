from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase, APIClient
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import AdminActivityLog
from rest_framework import status
from django.urls import reverse
User = get_user_model()


class PromoteUserViewTests(APITestCase):
    def setUp(self):
        # کاربر پروموتر که قراره بقیه رو ارتقا بده
        self.promoter = User.objects.create_user(
            username='adminuser',
            email='admin1@email.com',
            phone='+989121234567',
            national_id='3333333333',
            slug='admin1-user'
        )

        # گروهی که دسترسی داره
        group, _ = Group.objects.get_or_create(name='SuperUser')
        self.promoter.groups.add(group)

        # کاربری که قراره پروموت بشه
        self.target_user = User.objects.create_user(
            username='targetuser',
            email='target1@email.com',
            phone='+989121234568',
            national_id='2222222222',
            slug='target1-user'
        )

        self.url = reverse('promote-user')  # باید این نام در urls تعریف شده باشه
        self.client.force_authenticate(user=self.promoter)

    def test_promote_to_supportpanel(self):
        response = self.client.post(self.url, {
            "email": self.target_user.email,
            "group_name": "SupportPanel"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.target_user.groups.filter(name="SupportPanel").exists())

    def test_promote_to_superuser(self):
        response = self.client.post(self.url, {
            "email": self.target_user.email,
            "group_name": "SuperUser"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.target_user.groups.filter(name="SuperUser").exists())

    def test_user_already_superuser(self):
        self.target_user.is_superuser = True
        self.target_user.save()

        response = self.client.post(self.url, {
            "email": self.target_user.email,
            "group_name": "SuperUser"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_promote_user_does_not_exist(self):
        response = self.client.post(self.url, {
            "email": "notfound@example.com",
            "group_name": "SupportPanel"
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_group_name(self):
        response = self.client.post(self.url, {
            "email": self.target_user.email,
            "group_name": "InvalidGroup"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_without_permission(self):
        self.client.logout()

        normal_user = User.objects.create_user(
            username='normal',
            email='normal1@email.com',
            phone='+989121234569',
            national_id='4444444444',
            slug='normal1-user'
        )

        self.client.force_authenticate(user=normal_user)

        response = self.client.post(self.url, {
            "email": self.target_user.email,
            "group_name": "SupportPanel"
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





class RegisterAccountViewTests(APITestCase):
    
    def test_register_user(self):
        url = reverse("create-account")
        data = {
            "username": "normaluser_@12",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "phone":'+989121234561',
            "email": "normal1212@email.com",
            "about_me": "Normaluser....",
            "national_id": "8888888888",
            "gender": "male"
        }

        response = self.client.post(url, data, format='json')
    

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"]["username"], "normaluser_@12")
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

        user = User.objects.get(username="normaluser_@12")
        self.assertEqual(user.groups.count(), 0)
       
    def test_register_user_cannot_groups(self):
        url = reverse("create-account")    

        data = {
            "username": "baduser@_22",
            "first_name": "Reza",
            "last_name": "Karimi",
            "phone": "+989961232542",
            "email": "reza2@email.com",
            "about_me": "",
            "national_id": "7777777777",
            "gender": "male",
            "group": "anything"
        }

        response = self.client.post(url , data, format="json")
          
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("group", response.data)
        self.assertEqual(str(response.data["group"][0]), "Group field should not be included in registration data.")





class LogOutViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Logoutuser", password="strongpass123", phone="+989351161152"
        )
        
        self.refresh=RefreshToken.for_user(self.user)
        self.access_token=str(self.refresh.access_token)
        self.refresh_token=str(self.refresh)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.url=reverse("logging-Out")

    def test_user_can_logout_successfully(self):
        data = {"refresh_token":self.refresh_token}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "User Logged Out Successfully!")


    def test_logout_missing_refresh_token(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Refresh token is required.")        


    def test_logout_invalid_refresh_token(self):
        response = self.client.post(self.url, {"refresh_token": "fake-token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("Error during logout", response.data["detail"])    







class AdminActivityLogTests(APITestCase):
    def setUp(self):
        # ایجاد گروه‌ها
        self.supportpanel_group = Group.objects.create(name="SupportPanel")
        self.SuperUser_group = Group.objects.create(name="SupperUser")

        # ساخت کاربر support_user و افزودن به گروه SupportPanel
        self.support_user = User.objects.create_user(
            username="support_@1", password="testali1",
            email="testali2@email.com", phone="+989955431203",
            national_id="5555555555"
        )
        self.support_user.groups.add(self.supportpanel_group)

        # ساخت کاربر admin_user و افزودن به گروه SuperUser
        self.admin_user = User.objects.create_superuser(
            username="admin@12", password="adminpass",
            email="testadmin1@email.com", phone="+989124321204",
            national_id="6666666666", slug="test-ali4"
        )
        self.admin_user.groups.add(self.SuperUser_group)

        # ایجاد لاگ‌های مختلف
        self.recent_log = AdminActivityLog.objects.create(
            admin_user=self.support_user,
            action="Login",
            detail="Recent login",
            ip_address="127.0.0.1",
            user_agent="test-agent"
        )

        # ایجاد لاگ قدیمی‌تر
        old_date = now() - timedelta(days=4)
        self.old_log = AdminActivityLog.objects.create(
            admin_user=self.support_user,
            action="Login",
            detail="Old login",
            ip_address="127.0.0.1",
            user_agent="test-agent2",
            created_at=old_date
        )

        # URL برای دسترسی به لاگ‌ها
        self.url = reverse("admin-activity-logs")

    # def test_superuser_can_see_recent_logs_only(self):
    #     # وارد شدن به سیستم به عنوان admin_user (عضو گروه SuperUser)
    #     self.client.force_authenticate(user=self.admin_user)
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

        # # دریافت نتایج و بررسی صحت
        # results = response.data["results"]
        # self.assertEqual(len(results), 1)  # انتظار داریم فقط 1 لاگ (Recent login) نمایش داده شود
        # self.assertEqual(results[0]["detail"], "Recent login")

    def test_user_without_supperuser_group_denied(self):
        # ایجاد یک کاربر معمولی بدون گروه SuperUser
        normal_user = User.objects.create_user(
            username="user", password="pass",
            phone="+989123456789", national_id="1122334455",
            email="user@example.com"
        )
        self.client.force_authenticate(user=normal_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_cannot_access(self):
        # کاربر خارج از سیستم (بدون لاگین)
        self.client.logout()  
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)





