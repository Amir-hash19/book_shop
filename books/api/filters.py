from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from ..models import Book, Comment 
from django.db.models import Count





class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='incontains')
    author = filters.CharFilter(field_name='author__username', lookup_expr='exact')
    created_date = filters.DateFilter(field_name='created_date', lookup_expr='gte')
    is_published = filters.BooleanFilter(field_name='is_published')


    class Meta:
        model = Book
        fields = ["title", "author__username", "created_date", "is_published"]




