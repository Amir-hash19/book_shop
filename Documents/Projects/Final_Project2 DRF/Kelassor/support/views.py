from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (TicketSerializer ,TicketMessageCreateSerializer, TicketMessageSerializer, 
AdminEditableTicketMessageSerializer, TicketMessageCreateSerializer)
from account.permissions import GroupPermission, create_permission_class
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Ticket, TicketMessage
from account.views import CustomPagination
from django.http import Http404
from account.utils.logging import log_admin_activity
from rest_framework.exceptions import ValidationError
from rest_framework import status, serializers
from rest_framework.response import Response
from django.db import transaction
from rest_framework.exceptions import NotFound
from bootcamp.models import Bootcamp, BootcampRegistration
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend




#test passed
class CreateTickectView(CreateAPIView):
    """ساختن تیکت توسط کاربر"""
    # queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )
    def get_queryset(self):
        with transaction.atomic():
            return Ticket.objects.all()


#test passed
class DeleteTicketView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    lookup_field = 'slug'
    
    def get_object(self):
        return get_object_or_404(Ticket,
        slug=self.kwargs["slug"], user=self.request.user)



#test passed
class ListTicketView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "slug"]
    filterset_fields = ["created_at", "status"]
    ordering_fields = ["created_at"]
    def get_queryset(self):   
        return Ticket.objects.filter(user=self.request.user).order_by("-create_at")
    
        


#test passed
class EditTicketView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

        

#test passed
class CreateTicketMessageView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TicketMessageSerializer
    
    def perform_create(self, serializer):
        with transaction.atomic():
            ticket_slug = self.kwargs.get('slug')

        try:
            ticket = Ticket.objects.get(slug=ticket_slug)
        except Ticket.DoesNotExist:
            raise NotFound("Ticket not found!")

        if ticket.user != self.request.user:
            raise NotFound("You can only choose your ticket")

        serializer.save(ticket=ticket,
        sender=self.request.user)



#test passed
class ListTicketMessageView(ListAPIView):
    queryset = TicketMessage.objects.all().order_by("-created_at")
    serializer_class = TicketMessageCreateSerializer
    permission_classes = [IsAuthenticated, create_permission_class(["support.view_ticketmessage"])]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["message", "title"]
    filterset_fields = ["created_at", "message_status"]
    ordering_fields = ["created_at"]
    



        
#test passed
class AdminResponseMessageView(UpdateAPIView):
    queryset = TicketMessage.objects.all()
    permission_classes = [IsAuthenticated, create_permission_class(["support.change_ticketmessage"])]
    serializer_class = AdminEditableTicketMessageSerializer
    lookup_field = 'slug'
    def perform_update(self, serializer):
        with transaction.atomic():
            message = serializer.save(admin=self.request.user)
            try:
                log_admin_activity(
                    request=self.request,
                    action="updated ticket message",
                    instance=f"TicketMessage ID: {message.id}, Slug: {getattr(message, 'slug', 'N/A')}"
                )
            except Exception:
                pass
  


        


#test passed
class AdminDetailMessageView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, create_permission_class(["support.view_ticketmessage"])]
    queryset = TicketMessage.objects.all()
    serializer_class = TicketMessageSerializer
    lookup_field = 'slug'
    



class ListTicketMessageView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketMessageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["message", "title"]
    filterset_fields = ["created_at", "message_status"]
    ordering_fields = ["created_at"]    

    def get_queryset(self):
        return TicketMessage.objects.filter(sender=self.request.user)





class DetailTicketMessageView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketMessageSerializer
    lookup_field = "slug"
    def get_queryset(self):
        return TicketMessage.objects.filter(sender=self.request.user)

    