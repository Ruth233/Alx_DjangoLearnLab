from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

# Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # ✅ check for this
    confirm_password = serializers.CharField(write_only=True)  # ✅ check for this too

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'bio', 'profile_picture']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        user.bio = validated_data.get('bio', '')
        user.profile_picture = validated_data.get('profile_picture', None)
        user.save()

        Token.objects.create(user=user)
        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # ✅ check for this
    password = serializers.CharField(write_only=True)  # ✅ check for this too

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials.")
