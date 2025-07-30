from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from books.models import Book, Comment
from books.api.serializers import CommentSerializer, BookSerializer, CreateUserAccountSerializer
from books.api.permissions import IsAdminUserOrReadOnly, IsCommenterOrReadOnly
from rest_framework.permissions import AllowAny
from books.api.pagination import MySPagination, MyLPagination
from .filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from django.db import transaction
from .throttles import SignUpRatethrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by("created_date")
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = MySPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["created_date", "up_date"]
    filterset_class = BookFilter





class CreateUserAccountView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [SignUpRatethrottle]
    
    @transaction.atomic
    def psot(self, request):
        serializer = CreateUserAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {"detail":"User Account Created Successfully.",
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                }
                
            ), status.HTTP_201_CREATED
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










#We dont need to specify any pk because GenericAPIView already knows that we are going to use a pk.
class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        book_pk = self.kwargs.get('book_pk')
        #If there is a book with the id, it will return it. If not, it will return 404.
        book = generics.get_object_or_404(Book, pk=book_pk)
        user = self.request.user
        comments = Comment.objects.filter(book=book, commenter=user)
        if comments.exists():
            raise ValidationError('You have already commented on this book.')
        #It has a related object as a book. That's why, we can give the book.
        serializer.save(book=book, commenter=user)

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer 
    permission_classes = [IsCommenterOrReadOnly]       

#We dont need to use all of these. We can do everything with the above class.
# class BookListCreatorView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
    
#     #List all books
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     #Create a new book
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)