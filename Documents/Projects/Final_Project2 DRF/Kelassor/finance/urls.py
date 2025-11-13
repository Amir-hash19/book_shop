from django.urls import path
from .views import( CreateInvoiceView, ListUserWithInvoiceView, DeleteInvoiceView,
                    CreatePaymentView, AdminListPaymentView, ListPaymentView, 
                    ListTransactionView, EditInvoicesView, ListInvoiceUserView,
                      DetailInvoiceView, DetailTransactionView, DetailPaymentView)


urlpatterns = [
    path("create-invoice/", CreateInvoiceView.as_view(), name="create-invoice-for-user-by-admin"),
    path("list-users-invoices/", ListUserWithInvoiceView.as_view(), name="list-users-with-invoices"),
    path("delete-invoice/<slug:slug>/", DeleteInvoiceView.as_view(), name="delete-invoice-by-admin"),
    path("create/<slug:slug>/payment/", CreatePaymentView.as_view(), name="create-payment"),
    path("list-payments/", AdminListPaymentView.as_view(), name="list-payments-for-admin"),
    path("list-payments-user/", ListPaymentView.as_view(), name="list-payment-user"),
    path("list-transactions/", ListTransactionView.as_view(), name="list-transactions-user"),
    path("edit-invoices/<slug:slug>/", EditInvoicesView.as_view(), name="edit-invoices-by-admin"),
    path("list-invoice-user/", ListInvoiceUserView.as_view(), name="list-invoices-user"),
    path("detail-invoice-user/<slug:slug>/", DetailInvoiceView.as_view(), name="detail-invoice"),
    path("detail-transaction-user/<slug:slug>/", DetailTransactionView.as_view(), name="detail-transaction"),
    path("detail-payment-user/<slug:slug>/", DetailPaymentView.as_view(), name="detail-payment-user"),


]
