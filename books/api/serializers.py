from rest_framework import serializers
from books.models import Book, Comment
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.password_validation import validate_password

class CommentSerializer(serializers.ModelSerializer):
    #We can use this to get the name of the user.
    commenter = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        #fields = '__all__'
        #We exclude book because we only want to change the related book in the url.
        exclude = ['book',] 

class BookSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = '__all__'





class CreateUserAccountSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]


    def validate(self, attrs):
        if attrs["password"] != attrs["password"]:
            raise serializers.ValidationError({"password":"password do not match"})
        return attrs


    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user    
