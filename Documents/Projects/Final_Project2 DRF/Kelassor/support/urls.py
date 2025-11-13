from django.urls import path, include
from .views import (CreateTickectView, DeleteTicketView, ListTicketView, EditTicketView, CreateTicketMessageView,
CreateTicketMessageView, AdminResponseMessageView, AdminDetailMessageView, DetailTicketMessageView, ListTicketMessageView)
from rest_framework.routers import DefaultRouter
from .views import  ListTicketMessageView





urlpatterns = [
    path("add-ticket/", CreateTickectView.as_view(), name="create-tickect"),
    path("delete-ticket/<slug:slug>/", DeleteTicketView.as_view(), name="delete-ticket"),
    path("list-tickets/", ListTicketView.as_view(), name="list-tickets"),
    path("edit-ticket/<slug:slug>/", EditTicketView.as_view(), name="edit-ticket"),
    path("create-message/<slug:slug>/reply/", CreateTicketMessageView.as_view(), name="create-ticket-message"),
    path("list-ticket-message/", ListTicketMessageView.as_view(), name="list-ticket-message"),
    path("response-to-messages/<slug:slug>/", AdminResponseMessageView.as_view(), name="response-messages"),
    path("messages/details/<slug:slug>/", AdminDetailMessageView.as_view(), name="detail-message-for-admin"),
    path("ticket-message/list/", ListTicketMessageView.as_view(), name="list-ticket-massage-for-user"),
    path("ticket-message/detail/<slug:slug>/", DetailTicketMessageView.as_view(), name="detail-ticket-message-for-user"),

    
]
