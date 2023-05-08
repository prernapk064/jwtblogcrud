from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Blog
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

CustomUser = get_user_model()
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        user = self.user
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password','role',)
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username = validated_data["username"],
            email=validated_data['email'],
            password=validated_data['password'],
            role = validated_data['role']
        )
        return user
    def update(self, validate_data, request):
        data = self.context['request'].GET
        user = validate_data
        user.username = data["username"] if "username" in data else user.username
        user.email = data["email"] if "email" in data else user.email
        user.save()
    
       
        return user



class BlogSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Blog
        fields = ('id','title', 'text', 'image', 'author')
        read_only_fields = ('created_at', 'updated_at')

    
    def validate_author(self, value):
    #     """
    #     Check that the authenticated user is either the author or an admin/manager
    #     """
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication credentials were not provided.")
        if user.is_superuser or user.is_active or value == user:
            return value
        raise serializers.ValidationError("You do not have permission to perform this action.")

  
    def create(self, validated_data):
        blog = Blog(
            title=validated_data['title'],
            text=validated_data['text'],
            image=validated_data.get('image', None),
            author=self.context['request'].user
        )
        blog.save()
        return blog
        
        

    def update(self, validate_data, request):
        data = self.context['request'].GET
        user = validate_data
        user.title = data["title"] if "title" in data else user.title
        user.text = data["text"] if "text" in data else user.text
        user.image = data["image"] if "image" in data else user.image
        user.save()
        return user
