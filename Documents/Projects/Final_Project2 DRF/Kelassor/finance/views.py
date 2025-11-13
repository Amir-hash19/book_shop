from .models import Payment, Invoice, Transaction
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from account.permissions import GroupPermission, GroupHasDynamicPermission, create_permission_class
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status 
from account.views import CustomPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from account.utils.logging import log_admin_activity
from django_filters.rest_framework import DjangoFilterBackend
from account.views import CustomPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db import transaction
from rest_framework.exceptions import ValidationError
from account.models import CustomUser
from django.db.models import Sum
from .serializers import (InvoiceSerializer, BasicUserSerializer, PaymentSerializer, TransactionSerializer, 
InvoiceUpdateSerializer, DetailTransactionSerializer)
from django.db.models import Count





#test passed
class CreateInvoiceView(CreateAPIView):
    """ساختن فاکتور برای کاربر توسط پنل ادمین"""
    permission_classes = [IsAuthenticated, create_permission_class(["finance.add_invoice"])]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.all()

    def perform_create(self, serializer):
        with transaction.atomic():
            invoice = serializer.save()
            try:
                log_admin_activity(
                    request=self.request,
                    action="created invoice",
                    instance=f"Invoice ID: {invoice.id}, Amount: {getattr(invoice, 'amount', 'N/A')}"
                )
            except Exception:
                pass




#test passed
class ListUserWithInvoiceView(ListAPIView):
    """لیست کاربران بدونه فاکتور """
    permission_classes = [IsAuthenticated, create_permission_class(["finance.view_invoice"])]
    serializer_class = BasicUserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = CustomPagination
    search_fields = ["username", "email", "phone"]
    filterset_fields = ["gander", "date_added"]
    ordering_fields = ["date_added"]


    def get_queryset(self):
        return CustomUser.objects.annotate(invoice_count=Count('invoice')).filter(invoice_count__gt=0).order_by("-date_joined")


#test passed
class DeleteInvoiceView(DestroyAPIView):
    permission_classes = [IsAuthenticated, create_permission_class(["finance.delete_invoice"])]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer     
    lookup_field = 'slug'   

    def perform_destroy(self, instance):
        with transaction.atomic():
            invoice_id = instance.id  # ذخیره شناسه قبل از حذف
            instance.delete()
            try:
                log_admin_activity(
                    request=self.request,
                    action="deleted invoice",
                    instance=f"Invoice ID: {invoice_id}"
                )
            except Exception:
                pass



#test passed
class CreatePaymentView(CreateAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]


    def perform_create(self, serializer):
        with transaction.atomic():
            invoice_slug = self.kwargs.get('slug')
            try:
                invoice = Invoice.objects.select_for_update().get(slug=invoice_slug)
            except Invoice.DoesNotExist:
                raise ValidationError({"invoice":"the invoice does not existed!"})

            total_paid = invoice.payments.filter(is_verified=True).aggregate(
                total=Sum('amount'))['total'] or 0

            new_payment_amount = serializer.validated_data['amount']

            if total_paid + new_payment_amount > invoice.amount:
                raise ValidationError("This payment is exceeds the invoice total")


            if invoice.client != self.request.user:
                raise ValidationError("You can only select your invoice")


            payment = serializer.save(user=self.request.user, invoice=invoice)

            
            if total_paid + new_payment_amount >= invoice.amount:
                invoice.is_paid = True
                invoice.save()

            



#test passed
class AdminListPaymentView(ListAPIView):
    queryset = Payment.objects.all().order_by("-paid_at")
    permission_classes = [IsAuthenticated, create_permission_class(["finance.view_payment"])]
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["user__username", "invoice", "paid_at"]
    filterset_fields = ["is_verified", "method"]
    ordering_fields = ["paid_at"]

    

#test passed
class ListPaymentView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["amount", "invoice"]
    filterset_fields = ["method", "paid_at"]
    ordering_fields = ["paid_at"]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by("-paid_at")
    

#test passed
class ListTransactionView(ListAPIView):
    """لیست تراکنش های کاربر """
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "amount"]
    filterset_fields = ["transaction_type", "transaction_date"]
    ordering_fields = ["transaction_date"]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by("-transaction_date")
    

#test passed
class EditInvoicesView(UpdateAPIView):
    permission_classes = [IsAuthenticated, create_permission_class(["finance.change_invoice"])]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceUpdateSerializer
    lookup_field = 'slug'

    def perform_update(self, serializer):
        with transaction.atomic():
            invoice = serializer.save()
            try:
                log_admin_activity(
                    request=self.request,
                    action="updated invoice",
                    instance=f"Invoice ID: {invoice.id}, Amount: {getattr(invoice, 'amount', 'N/A')}"
                )
            except Exception:
                pass


#test passed
class ListInvoiceUserView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceUpdateSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["description", "amount"]
    filterset_fields = ["is_paid", "created_at"]
    ordering_fields = ["created_at"]


    def get_queryset(self):
        return Invoice.objects.filter(client=self.request.user).order_by("-created_at")
    


#test passed
class DetailInvoiceView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    lookup_field = 'slug' 

    def get_queryset(self):
        return Invoice.objects.select_related('client').filter(client=self.request.user)
    

#test passed
class DetailTransactionView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DetailTransactionSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)




#test passed
class DetailPaymentView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)