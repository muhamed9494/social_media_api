from rest_framework import serializers
from .models import CustomUser, Post, Follow
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed_user', 'created_at']

    def validate(self, data):
        """
        Ensure that a user cannot follow themselves.
        """
        if data['follower'] == data['followed_user']:
            raise ValidationError("You cannot follow yourself.")
        return data


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'user', 'timestamp', 'media']

    def validate_content(self, value):
        """
        Optional: Ensure content is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Hashing the password before saving the user
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Use Django's authenticate function to check credentials
        """
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}
