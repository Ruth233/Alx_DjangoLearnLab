from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from .serializers import SimpleUserSerializer

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # return token in response
        token, _ = Token.objects.get_or_create(user=user)
        data = ProfileSerializer(user, context={'request': request}).data
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # return currently authenticated user
        return self.request.user

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """Authenticated user follows another user"""
        user_to_follow = generics.get_object_or_404(User, id=user_id)
        if request.user == user_to_follow:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(user_to_follow)
        return Response({"detail": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """Authenticated user unfollows another user"""
        user_to_unfollow = generics.get_object_or_404(User, id=user_id)
        request.user.following.remove(user_to_unfollow)
        return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
