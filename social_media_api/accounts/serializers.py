from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'bio', 'profile_picture']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        # ✅ REQUIRED: This line ensures password hashing and proper user creation
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

    # Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # ✅ check for this
    password = serializers.CharField(write_only=True)  # ✅ check for this too

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials.")
        user.bio = validated_data.get('bio', '')
        user.profile_picture = validated_data.get('profile_picture', None)
        user.save()

        # Create a token for the new user
        Token.objects.create(user=user)

        return user

class SimpleUserSerializer(serializers.ModelSerializer):
    follower_count = serializers.IntegerField(source='follower_count', read_only=True)
    following_count = serializers.IntegerField(source='following_count', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_picture', 'bio', 'follower_count', 'following_count')
        read_only_fields = ('id', 'username', 'follower_count', 'following_count')
