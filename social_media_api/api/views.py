from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth import authenticate, login, logout
from .models import Post, Follow, CustomUser
from .serializers import RegisterSerializer, LoginSerializer, FollowSerializer, PostSerializer
from rest_framework import status
from django.db import IntegrityError
from django.db.models import Q
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    """
    User ViewSet to handle user-related actions.
    Provides access to user data and their feed based on follows.
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def feed(self, request):
        """
        Retrieves posts from users that the authenticated user is following.
        """
        user = request.user
        followed_users = user.following.values_list('followed_user', flat=True)
        feed_posts = Post.objects.filter(Q(author__id__in=followed_users)).order_by('-created_at')
        return Response(PostSerializer(feed_posts, many=True).data)

class RegisterView(APIView):
    """
    Handles user registration.
    Allows users to create new accounts.
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                user.is_active = True
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"detail": "Username or email already taken."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    Handles user login.
    Authenticates users using username and password.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=request.data['username'], password=request.data['password'])
            if user is not None:
                login(request, user)
                return Response({"detail": "Login successful."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """
    Handles user logout.
    Logs the user out of the session.
    """
    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)

class FollowViewSet(viewsets.ModelViewSet):
    """
    Handles follow/unfollow actions.
    Allows users to follow other users.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        """
        Prevents users from following themselves.
        """
        if self.request.user == serializer.validated_data['following']:
            raise serializers.ValidationError("You cannot follow yourself.")
        serializer.save(follower=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    """
    Handles creating, retrieving, updating, and deleting posts.
    Only authenticated users can create posts, but everyone can view them.
    """
    queryset = Post.objects.all().order_by('-created_at')  # Adjust field name if necessary
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """
        Automatically sets the user as the author of the post.
        """
        serializer.save(author=self.request.user)
