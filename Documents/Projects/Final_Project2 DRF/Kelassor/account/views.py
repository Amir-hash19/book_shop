from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .OTPThrottle import OTPThrottle
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Group
from .models import CustomUser, AdminActivityLog
from .serializers import (CreateAccountSerializer, EditAccountSerializer, CustomAccountSerializer,
SupportPanelSerializer, OTPSerializer, VerifyOTPSerializer, PromoteUserSerializer, GroupPermissionSerializer,
AdminActivityLogSerializer)
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import GroupPermission, is_supportpanel_user, create_permission_class
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group, Permission
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.utils.timezone import now, timedelta
from collections import defaultdict
from rest_framework import status
from django.db import transaction
from .OTPThrottle import OTPThrottle
from .tasks import send_otp_task
from django.core.cache import cache
import json

class CustomPagination(PageNumberPagination):
    page_size = 20


class CreateGroupWithPermissions(APIView):
    """
    ساختن گروه  فقط با دسترسی سوپر یوزر قابل انجام هست این ویو یه گروه میسازه و یه لیست از دسترسی ها رو میگیره 
    """
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser")]

    def post(self, request):
        serializer = GroupPermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        group_name = serializer.validated_data['group_name']
        permission_codenames = serializer.validated_data['permissions']

        if Group.objects.filter(name=group_name).exists():
            return Response({'error': 'Group already exists'}, status=status.HTTP_400_BAD_REQUEST)

        group = Group.objects.create(name=group_name)

        permissions = Permission.objects.filter(codename__in=permission_codenames)
        if not permissions.exists():
            return Response({'error': 'No valid permissions found'}, status=status.HTTP_400_BAD_REQUEST)

        group.permissions.set(permissions)

        return Response({
            'message': f'Group "{group_name}" created with {permissions.count()} permissions.'
        }, status=status.HTTP_201_CREATED)





class GroupedPermissionListAPI(APIView):
    """
    برای ساختن گروه کاربر باید بتونه یه لیستی از دسترسی ها رو ببینه تا به گروه اضافه کن این کاربر با دادن اسم کد  دسترسی قابل انجام هست
    """
    permission_classes = [GroupPermission("SuperUser")]

    def get(self, request):
        basic_perms = ['add', 'change', 'delete', 'view']
        permissions = Permission.objects.select_related('content_type').all()

        grouped_data = defaultdict(list)

        for perm in permissions:
            codename = perm.codename
            if any(codename.startswith(prefix + '_') for prefix in basic_perms):
                app_label = perm.content_type.app_label
                grouped_data[app_label].append(codename)

        return Response(grouped_data)        





#test passed
#ساختن اکانت عادی برای کاربر نرمال 
class RegisterAccountView(APIView):
    """امکان ساختن اکانت برای کاربر و دریافت توکن بعد از ساختن همچنین برای جلوگیری از ذخیره اطلاعات ناقص از رول بک استفاده شده"""
    permission_classes = [AllowAny]
    def post(self, request):
        with transaction.atomic():
            serializer = CreateAccountSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                refresh = RefreshToken.for_user(user)

                return Response({
                    "user": serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                    },status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#test passed
#ویرایش اکانت برای کاربر عادی
class EditAccountView(UpdateAPIView):
    """ کاربر میتونه اکانت خودشو ادیت کنه اگه اهراز هویت شده باشه """
    permission_classes = [IsAuthenticated]
    serializer_class = EditAccountSerializer

    def get_object(self):
        return self.request.user
    


#برای خروج کاربر
class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "User Logged Out Successfully!"})
        except Exception:
            return Response({"detail": "Error during logout, please try again later."}, status=500)



class DeleteAccountView(DestroyAPIView):
    """ در جنگو پاک کردن نداریم"""
    permission_classes = [IsAuthenticated]
    serializer_class = CustomAccountSerializer

    def get_object(self):
        return self.request.user
    


#test passed
class DetailAccountView(RetrieveAPIView):
    """ کاربر میتونه اکانت خودشو ببینه  کنه اگه اهراز هویت شده باشه """
    permission_classes = [IsAuthenticated]
    serializer_class = CustomAccountSerializer


    def get_object(self):
        return self.request.user
    



#test passed
class ListSupportAccountView(ListAPIView):
    """همچنین کاربر سوپر یوزر میتونه لیستی از کاربران پنل ببینه """
    queryset = CustomUser.objects.filter(groups__name__in=["SupportPanel"]).order_by("-date_joined")
    permission_classes = [IsAuthenticated,create_permission_class(["support.view_customuser"])]
    serializer_class = SupportPanelSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["date_joined", "phone", "username", "last_name"]
    filterset_fields = ["date_joined", "birthday"]
    ordering_fields = ["-date_joined"]





class SendOTPLogInView(APIView):
    """ارسال کد یک بار مصرف برای ورود به سایت و دریافت توکن"""
    permission_classes = [AllowAny]
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = OTPSerializer(data=request.data) 

        if serializer.is_valid():
            phone = str(serializer.validated_data["phone"]) 


            send_otp_task.delay(phone)


            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






MAX_FAILED_ATTEMPTS = 5
BLOCK_TIME_SECONDS = 300  

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = str(serializer.validated_data["phone"])
            otp = serializer.validated_data["otp"]

            fail_key = f"otp_fail:{phone}"
            blocked = cache.get(fail_key)

            if blocked and int(blocked) >= MAX_FAILED_ATTEMPTS:
                return Response({"error": "Too many attempts. Please try again later."},
                                status=status.HTTP_429_TOO_MANY_REQUESTS)

            cached_otp = cache.get(f"otp:{phone}")
            if cached_otp and str(cached_otp) == otp:
                cache.delete(f"otp:{phone}")  
                cache.delete(fail_key)  

             
                user = get_user_model().objects.filter(phone=phone).first()
                if not user:
                    return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

                refresh = RefreshToken.for_user(user)


                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                })

            else:
                # افزایش شمارنده تلاش ناموفق
                current_fails = cache.get(fail_key, 0)
                cache.set(fail_key, int(current_fails) + 1, timeout=BLOCK_TIME_SECONDS)

                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class PromoteUserView(APIView):
    """امکان دادن دسترسی با اضافه کردن کاربر به گروه خاص"""
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser")]

    
    def post(self, request):
        # دریافت داده‌ها از serializer
        serializer = PromoteUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            group_name = serializer.validated_data.get("group_name")
            
            # بررسی وجود کاربر با ایمیل وارد شده
            try:
                user = CustomUser.objects.get(email__iexact=email)
            except CustomUser.DoesNotExist:
                return Response({"detail": "Email does not exist!"}, status=status.HTTP_404_NOT_FOUND)

            # اگر کاربر قبلاً سوپر یوزر است
            if user.is_superuser:
                return Response({"detail": "This User is already a SuperUser!"}, status=status.HTTP_400_BAD_REQUEST)

            # گرفتن کاربر درخواست‌دهنده
            requesting_user = request.user

            # بررسی اینکه کاربر درخواست‌دهنده عضو گروه SuperUser باشد
            if not requesting_user.groups.filter(name="SuperUser").exists():
                return Response({"detail": "You do not have permission to promote users to SuperUser!"}, status=status.HTTP_403_FORBIDDEN)

            # اضافه کردن کاربر به گروه‌ها و تغییر ویژگی‌های آن‌ها
            group_name = serializer.validated_data.get("group_name")  # فرض بر این است که گروه در داده‌ها موجود باشد
            group, _ = Group.objects.get_or_create(name=group_name)

            if group.name == 'SuperUser':
                user.is_superuser = True
            elif group.name == 'SupportPanel':
                user.is_staff = True

            # اضافه کردن کاربر به گروه
            user.groups.add(group)
            user.save()

            return Response({
                "detail": f"User {user.email} has been promoted successfully to {group.name}."
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


#tast passed
class DeleteSupportPanelView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser")]
    serializer_class = SupportPanelSerializer
    lookup_field = 'slug'

    def perform_destroy(self, instance):
        if self.request.user == instance:
            raise ValidationError("You Cannot Delete your own account from here!")
        



class AdminLogOutView(APIView):
    permission_classes = [IsAuthenticated,GroupPermission("SuperUser", "SupportPanel")]
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({"details":"User Logged Out Successfully!"})
        except Exception as e:
            return Response({"details": "Error during logout, please try again later."}, status=500)





#test passed
class ListAdminActivityLogView(ListAPIView):
    """دیدن لیستی از فعالیت های چند ساعت اخیر کاربر عضو گروه پنل"""
    serializer_class = AdminActivityLogSerializer
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser")]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["action", "detail", "admin_user__username", "admin_user__phone"]
    filterset_fields = ["created_at"]
    ordering_fields = ["created_at"]



    def get_queryset(self):
        last_72_hours = now() - timedelta(hours=72)

        return AdminActivityLog.objects.filter(
            admin_user__groups__name="SupportPanel",
            created_at__gte=last_72_hours
        ).order_by("-created_at")