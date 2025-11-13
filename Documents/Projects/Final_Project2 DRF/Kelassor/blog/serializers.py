from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Blog, CategoryBlog





class BlogCategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryBlog
        fields = ["name"]
        




class UploadBlogSerializer(serializers.ModelSerializer):
    blogcategory = serializers.SlugRelatedField(
        slug_field = "name",
        queryset=CategoryBlog.objects.all()
    )
    uploaded_by = serializers.StringRelatedField()
    class Meta:
        model = Blog
        fields = ['title', 'content',  'blogcategory', 'uploaded_by', "file", "date_added"]
        read_only_fields = ['uploaded_by', 'slug'] 




class BlogSerializer(serializers.ModelSerializer):
    blogcategory = serializers.SlugRelatedField(
        slug_field='name',
        queryset=CategoryBlog.objects.all() 
    )
    uploaded_by = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = "__all__"