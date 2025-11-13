from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (AdminCreateBootcampView, AdminCreateCategoryView, AdminEditCategoryView,
                    AdminDeleteCategoryView, AdminEditBootCampView, AdminDeleteBootCampView, 
                    ListAvailableBootCampViewSet, ListCategoryBootcampView, AdminListAllBootCampView,
                    DetailBootCampView, MostRequestedBootCampView, ListBootCampRegistrationView, 
                    BootcampCategoryViewSet, CreateBootcampRegistrationView, CheckRegistraionStatusView, 
                    BootcampApprovedStudentsListView, ListSMSLogView, DeleteSMSLogView, MassNotificationView)

router = DefaultRouter()
router.register(r'bootcamps', ListAvailableBootCampViewSet, basename='bootcamp')
router.register(r'bootcampcategories', BootcampCategoryViewSet, basename='bootcampcategory')


urlpatterns = [
    path("add-bootcamp/", AdminCreateBootcampView.as_view(), name="create-bootcamp-by-admin"),
    path("add-category/", AdminCreateCategoryView.as_view(), name="create-category-by-admin"),
    path("edit-category/<slug:slug>/", AdminEditCategoryView.as_view(), name="edit-bootcamp-by-admin"),
    path("delete-bootcamp-category/<slug:slug>/", AdminDeleteCategoryView.as_view(), name="delete-bootcamp-category-by-superuser"),
    path("edit-bootcamp/<slug:slug>/", AdminEditBootCampView.as_view(), name="edit-bootcamp-by-admin"),
    path("delete-bootcamp/<slug:slug>/", AdminDeleteBootCampView.as_view(), name="delete-bootcamp-by-admin"),
    path("list-category-bootcamp/", ListCategoryBootcampView.as_view(), name="list-bootcamp-category"),
    path("list-all-bootcamps/", AdminListAllBootCampView.as_view(), name="list-all-bootcamps-for-admin"),
    path("detail-bootcamp/<slug:slug>/", DetailBootCampView.as_view(), name="detail-bootcamp"),
    path("most-registered-bootcamp/", MostRequestedBootCampView.as_view(), name="list-most-registred-bootcamp"),
    path("bootcamp-signup/", CreateBootcampRegistrationView.as_view(), name="registration-bootcamp"),
    path("list-bootcamp-registration/", ListBootCampRegistrationView.as_view(), name="list-boortcamp-regitration"),
    path("check-registration-status/<slug:slug>/", CheckRegistraionStatusView.as_view(), name="check-status-registrations"),
    path("bootcamps/approved-students/<slug:slug>/", BootcampApprovedStudentsListView.as_view(), name="students-bootcamp"),
    path("delete-smslog/", DeleteSMSLogView.as_view(), name="delete-smslog-for-admin"),
    path("create-notification/", MassNotificationView.as_view(), name="create-notify-by-admin"),
    path("list-SMSLog/", ListSMSLogView.as_view(), name="SMS-log-for-admin"),
    path('', include(router.urls)), 
     

]
