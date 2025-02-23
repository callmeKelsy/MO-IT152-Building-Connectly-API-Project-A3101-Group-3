from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Post, Comment, User

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# User list and create view
class UserListCreate(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Add any logic you need here for user creation
        serializer.save()

# User detail view
class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Post serializer
class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)  # Only return author ID

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_type', 'author', 'metadata']

# Post list and create view
class PostListCreate(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """ Auto-assigns the authenticated user as the post author """
        serializer.save(author=self.request.user)

# Post detail view
class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

# Comment serializer
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)  # Auto-assign author ID
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)  # Auto-assign post ID

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'created_at']

    def create(self, validated_data):
        """ Auto-assign post from view """
        post = self.context.get('post')
        if not post:
            raise serializers.ValidationError({"post": "This field is required."})
        return Comment.objects.create(post=post, **validated_data)

# Comment list and create view
class CommentListCreate(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Auto-assigns the authenticated user as the comment author """
        serializer.save(author=self.request.user)

# Comment detail view
class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

# Optional: If you really want a separate CreatePostView
class CreatePostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Custom logic to create a post """
        serializer.save(author=self.request.user)

# views.py
from rest_framework.generics import ListAPIView
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated

# PostCommentsView to list all comments related to a specific post
class PostCommentsView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id)

# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Login view (dummy example, you can modify this as per your logic)
@api_view(['POST'])
def login_user(request):
    # Here you can handle login logic
    # For example, you can authenticate the user and return a token or session.
    return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"message": "This is a protected admin view!"})

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view!"})

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

# List all users (GET request)
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Change this based on authentication needs

# Create a new user (POST request)
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

from django.shortcuts import render
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the POST data
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Add your authentication logic here
        
        return JsonResponse({"message": "Login successful"})  # Or return appropriate response
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)



