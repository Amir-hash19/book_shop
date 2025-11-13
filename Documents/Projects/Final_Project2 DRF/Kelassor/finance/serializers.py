from rest_framework.serializers import ModelSerializer
from .models import Invoice, Transaction, Payment
from rest_framework import serializers
from account.models import CustomUser
from django.db import transaction




class InvoiceSerializer(ModelSerializer):
    client = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all()
    )
    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ["slug"]





class BasicUserSerializer(serializers.ModelSerializer):
    invoice_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', "invoice_count"]




class PaymentSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    invoice = serializers.StringRelatedField()
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["slug", "user", "invoice"]

    def validate(self, data):
        method = data.get("method")
        tracking_code = data.get("tracking_code")
        receipt_image = data.get("receipt_image")


        if method == "offline" and (not tracking_code or not receipt_image):
            raise serializers.ValidationError("Please upload your picture and tracking code")
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            validated_data["user"] = self.context["request"].user
            return super().create(validated_data)    




class TransactionSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Transaction
        fields = ["user", "amount", "description", "transaction_date", "transaction_type", "is_verified"]



class InvoiceUpdateSerializer(ModelSerializer):
    client = serializers.StringRelatedField()
    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ["client", "amount", "deadline", "description", "created_at", "slug"]


    def update(self, instance, validated_data):
        is_paid = validated_data.get('is_paid', None)
        if is_paid is not None:
            instance.is_paid = is_paid    

        instance.save()
        return instance    
    




class DetailTransactionSerializer(ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Transaction
        fields = "__all__"