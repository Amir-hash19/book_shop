from .models import CategoryBlog
import django_filters





class CategoryBlogFilter(django_filters.FilterSet):
    date_created = django_filters.DateFilter(field_name='date_created', lookup_expr='date')


    class Meta:
        model = CategoryBlog
        fields = ["date_created"]