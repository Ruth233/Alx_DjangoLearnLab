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

User = get_user_model()

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """Current user follows user with id=user_id"""
        if request.user.id == user_id:
            return Response({"detail": "Cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        target = generics.get_object_or_404(User, id=user_id)
        request.user.following.add(target)
        return Response({"detail": f"You are now following {target.username}"}, status=status.HTTP_200_OK)

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """Current user unfollows user with id=user_id"""
        target = generics.get_object_or_404(User, id=user_id)
        request.user.following.remove(target)
        return Response({"detail": f"You have unfollowed {target.username}"}, status=status.HTTP_200_OK)

class FollowersListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SimpleUserSerializer

    def get_queryset(self):
        user = generics.get_object_or_404(User, id=self.kwargs['user_id'])
        return user.followers.all()

class FollowingListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SimpleUserSerializer

    def get_queryset(self):
        user = generics.get_object_or_404(User, id=self.kwargs['user_id'])
        return user.following.all()
