from django.urls import path
from .views import (RegisterAccountView, EditAccountView, LogOutView, DeleteAccountView, DetailAccountView, 
ListSupportAccountView, ListAdminActivityLogView, SendOTPLogInView, VerifyOTPView, PromoteUserView,
DeleteSupportPanelView, AdminLogOutView, CreateGroupWithPermissions, GroupedPermissionListAPI)
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path("create-account/", RegisterAccountView.as_view(), name="create-account"),
    path("edit-account/", EditAccountView.as_view(), name="edit-account"),
    path("refresh-token/", TokenRefreshView.as_view()), #موقت فقط برای توکن گرفتن 
    path("logout-account/", LogOutView.as_view(), name="logging-Out"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete-account"),
    path("detail-account/", DetailAccountView.as_view(), name="detail-account"),
    path("list-supportpanel-user/", ListSupportAccountView.as_view(), name="list-supportpanel-user"),
    path("loggin/", SendOTPLogInView.as_view(), name="send-otp"),
    path("verify-code/", VerifyOTPView.as_view(), name="verify-otp"),
    path("promote-to-user/", PromoteUserView.as_view(), name="promote-user"),
    path("delete-supportpanel-user/<slug:slug>/", DeleteSupportPanelView.as_view(), name="delete-supportpanel-user-by-superuser"),
    path("logout-admin/", AdminLogOutView.as_view(), name="logout-admin-view"),
    path("admin-activity-logs/", ListAdminActivityLogView.as_view(), name="admin-activity-logs"),
    path("groups/create/", CreateGroupWithPermissions.as_view(), name="create-group-by-admin"),
    path("permissions/lists/", GroupedPermissionListAPI.as_view(), name="list-permissions"),


]    
