# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture', 'token')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        # create token
        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Unable to authenticate with provided credentials.")
        else:
            raise serializers.ValidationError("Must include username and password.")
        token, _ = Token.objects.get_or_create(user=user)
        return {
            'username': user.username,
            'token': token.key,
            'user_id': user.id,
        }

class ProfileSerializer(serializers.ModelSerializer):
    follower_count = serializers.IntegerField(source='follower_count', read_only=True)
    following_count = serializers.IntegerField(source='following_count', read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'follower_count', 'following_count')
        read_only_fields = ('username', 'follower_count', 'following_count')
