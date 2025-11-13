from rest_framework.serializers import ModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from django.db import IntegrityError
from django.db import transaction
from .models import CustomUser, AdminActivityLog

User = get_user_model()



class CreateAccountSerializer(serializers.ModelSerializer):
    group = serializers.CharField(required=False)
   

    class Meta:
        model = CustomUser
        fields = [
            "username", "first_name", "last_name", "phone", "email",
            "about_me", "national_id", "gender","group"
        ]
        read_only_fields = ['group']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["phone"] = str(instance.phone) 
        return data
    
    def validate_group(self, value):
        raise serializers.ValidationError("Group field should not be included in registration data.")


    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("group", None)  # فقط برای اطمینان
        return CustomUser.objects.create(**validated_data)







class EditAccountSerializer(ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), many=True, required=False, write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "phone", "email",
                  "about_me", "national_id", "gender", "password", "groups"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        if not user.is_authenticated or not user.groups.filter(name__in=["superuser", "supportpanel"]).exists():
            self.fields.pop('groups', None)




class CustomAccountSerializer(ModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)
  
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name",
        "phone", "email", "about_me", "birthday", "gender", "national_id","date_joined", "groups","last_login"]
        read_only_fields = ["is_active", "is_superuser", "is_staff", "slug", "id", "groups"]

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            user = self.context['request'].user

            if not user.is_authenticated or not user.groups.filter(name__in=["superuser", "supportpanel"]).exists():
                self.fields.pop("groups")





class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name', 'codename']




class SupportPanelSerializer(ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    user_permissions = PermissionSerializer(many=True)
    class Meta:
        model = User
        fields = "__all__"





class OTPSerializer(serializers.Serializer):
    phone = PhoneNumberField(region="IR")
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['phone'] = str(instance.phone)
        return representation
    



class VerifyOTPSerializer(serializers.Serializer):
    phone = PhoneNumberField(region="IR")
    otp = serializers.CharField(max_length=6)




class PromoteUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    group_name = serializers.CharField()


    def validate_email(self, value):
        value = value.lower().strip()
        if not value:
            raise serializers.ValidationError("email Can not be empty!")
        return value
        


 

class AdminActivityLogSerializer(serializers.ModelSerializer):
    admin_user = serializers.StringRelatedField()
    class Meta:
        model = AdminActivityLog
        fields = "__all__"




class GroupPermissionSerializer(serializers.Serializer):
    group_name = serializers.CharField(max_length=150)
    permissions = serializers.ListField(
        child=serializers.CharField(max_length=100),
        allow_empty=False
    )

