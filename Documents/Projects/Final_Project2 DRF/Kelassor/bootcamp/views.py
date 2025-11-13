from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from account.permissions import GroupPermission, create_permission_class
from account.views import CustomPagination
from account.utils.logging import log_admin_activity
from rest_framework import viewsets
from .models import BootcampCategory, Bootcamp, BootcampRegistration, SMSLog
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .serializers import (BootcampSerializer,CategoryBootcampSerializer, BootcampCountSerializer,BootcampCategorySerializer,BootcampRegistrationCreateSerializer,
AdminBootcampRegistrationSerializer, BootCampRegitrationSerializer, BootcampStudentSerializer,
SMSLogSerializer, MassNotificationSerializer)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from django.db.models import Count
from django.utils import timezone
from django.http import Http404
from django.db import transaction


#test passed
class AdminCreateBootcampView(CreateAPIView):
    """ ساختن بوت کمپ توسط پنل ادمین و سوپر یوزر"""
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.add_bootcamp"])]
    serializer_class = BootcampSerializer

    def get_queryset(self):
        return Bootcamp.objects.all()

    def perform_create(self, serializer):
            bootcamp = serializer.save()
            try:
                log_admin_activity(
                    request=self.request,
                    action="created bootcamp",
                    instance=f"Bootcamp ID: {bootcamp.id}, Name: {bootcamp.name}"
                )
            except Exception:
                pass




#test passed
class AdminCreateCategoryView(CreateAPIView):
    """ ساختن دسته بندی بوت کمپ توسط پنل ادمین و سوپر یوزر"""
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.add_bootcampcategory"])]
    serializer_class = CategoryBootcampSerializer
    queryset = BootcampCategory.objects.all()

    def perform_create(self, serializer):
        with transaction.atomic():
            category = serializer.save()
            try:
                log_admin_activity(
                    request=self.request,
                    action="created bootcamp category",
                    instance=f"Category ID: {category.id}, Name: {category.name}"
                )
            except Exception:
                pass
    


#test passed
class AdminEditCategoryView(UpdateAPIView):
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.change_bootcampcategory"])]
    serializer_class = CategoryBootcampSerializer
    queryset = BootcampCategory.objects.all()
    lookup_field = 'slug'

    def perform_update(self, serializer):
 
            category = serializer.save()
            try:
                log_admin_activity(
                    request=self.request,
                    action="updated bootcamp category",
                    instance=f"Category ID: {category.id}, Name: {category.name}"
                )
            except Exception:
                pass


#test passed
class AdminDeleteCategoryView(DestroyAPIView):
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.delete_bootcampcategory"])]
    serializer_class = CategoryBootcampSerializer
    queryset = BootcampCategory.objects.all()
    lookup_field = 'slug'

    def perform_destroy(self, instance):
  
            category_name = instance.name
            instance.delete()
            try:
                log_admin_activity(
                    request=self.request,
                    action="deleted bootcamp category",
                    instance=category_name
                )
            except Exception:
                pass




#test passed
class AdminEditBootCampView(UpdateAPIView):
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.change_bootcamp"])]
    serializer_class = BootcampSerializer
    queryset = Bootcamp.objects.all()
    lookup_field = 'slug'

    def perform_update(self, serializer):

            bootcamp = serializer.save()
            try:
                log_admin_activity(
                    request=self.request,
                    action="updated bootcamp",
                    instance=f"Bootcamp ID: {bootcamp.id}, Name: {bootcamp.name}"
                )
            except Exception:
                pass





#test passed
class AdminDeleteBootCampView(DestroyAPIView):
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.delete_bootcamp"])]
    serializer_class = BootcampSerializer
    queryset = Bootcamp.objects.all()
    lookup_field = 'slug'

    def perform_destroy(self, instance):

            bootcamp_name = instance.name
            instance.delete()
            try:
                log_admin_activity(
                    request=self.request,
                    action="deleted bootcamp",
                    instance=bootcamp_name
                )
            except Exception:
                pass





#test passed
class ListAvailableBootCampViewSet(viewsets.ModelViewSet):
    queryset = Bootcamp.objects.filter(status="registering").order_by("-created_at")
    permission_classes = [AllowAny]
    serializer_class = BootcampSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "category", "created_at"]
    filterset_fields = ["is_online", "price"]
    ordering_fields = ["created_at"]
    lookup_field = 'slug'


#test passed
class BootcampCategoryViewSet(viewsets.ModelViewSet):
    queryset = BootcampCategory.objects.all()
    serializer_class = BootcampCategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'




#test passed
class ListCategoryBootcampView(ListAPIView):
    queryset = BootcampCategory.objects.all().order_by("-date_created")
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.view_bootcampcategory"])]
    serializer_class = CategoryBootcampSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    filterset_fields = ["date_created"]
    ordering_fields = ["date_created"]





#test passed
class AdminListAllBootCampView(ListAPIView):
    queryset = Bootcamp.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.view_bootcamp"])]
    serializer_class = BootcampSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    filterset_fields = ["status", "is_online", "category", "created_at"]
    ordering_fields = ["created_at"]




#test passed
class DetailBootCampView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = BootcampSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Bootcamp.objects.filter(status="registering")
     
    def get_object(self):
        try:
            return super().get_object()    
        except Http404:
            raise NotFound("Bootcamp not found !")





#test passed
class MostRequestedBootCampView(ListAPIView):
    serializer_class = BootcampCountSerializer
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.view_bootcamp"])]

    def get_queryset(self):
        return Bootcamp.objects.annotate(
        request_count=Count("registrations")
    ).order_by("-request_count")[:10]





#test passed
class ListBootCampRegistrationView(ListAPIView):
    queryset = BootcampRegistration.objects.filter(status='pending').order_by("-registered_at")
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.view_bootcampregistration"])]
    serializer_class = BootCampRegitrationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["phone_number", "comment"]
    filterset_fields = ["payment_type", "status", "reviewed_by"]
    ordering_fields = ["registered_at"]
    





#test passed
class CheckRegistraionStatusView(UpdateAPIView):
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.change_bootcampregistration"])]
    queryset = BootcampRegistration.objects.all()
    serializer_class = AdminBootcampRegistrationSerializer
    lookup_field = 'slug'

    def perform_update(self, serializer):
        with transaction.atomic():
            registration = serializer.save(
                reviewed_by=self.request.user,
                reviewed_at=timezone.now()
            )
            try:
                log_admin_activity(
                    request=self.request,
                    action="reviewed bootcamp registration",
                    instance=f"Registration ID: {registration.id}, User: {registration.user.username}"
                )
            except Exception:
                pass


#test passed
class CreateBootcampRegistrationView(CreateAPIView):
    queryset = BootcampRegistration.objects.all()
    serializer_class = BootcampRegistrationCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            volunteer=self.request.user
        )




#test passed
class BootcampApprovedStudentsListView(ListAPIView):#لیست اعضای یه بوت کمپ
    permission_classes = [IsAuthenticated, create_permission_class(["bootcamp.view_bootcamp"])]
    serializer_class = BootcampStudentSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        try:
            bootcamp = Bootcamp.objects.get(slug=slug)
        except Bootcamp.DoesNotExist:
            raise NotFound("BootCamp does Not existed!") 
        
        return BootcampRegistration.objects.filter(bootcamp=bootcamp, status='approved')   





#test passed
class ListSMSLogView(ListAPIView):
    queryset = SMSLog.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser", "SupportPanel")]
    serializer_class = SMSLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["phone_number", "full_name", "response_message"]
    filterset_fields = ["status", "created_at"]
    ordering_fields = ["created_at"]
    


#test passed
class DeleteSMSLogView(DestroyAPIView):
    """ پاک کردن لاگ های دیتابیس برای بالا بردن کیفیت """
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser", "SupportPanel")]
    queryset = SMSLog.objects.all()
    serializer_class = SMSLogSerializer
    lookup_field = "slug"



class MassNotificationView(APIView):
    permission_classes = [IsAuthenticated, GroupPermission("SuperUser", "SupportPanel")]



    def post(self, request):
            with transaction.atomic():
                serializer = MassNotificationSerializer(data=request.data)
                if serializer.is_valid():
                    notifications = serializer.save()
                return Response({
                    "detail": f"{len(notifications)} notifications created and are being sent."
                    }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)