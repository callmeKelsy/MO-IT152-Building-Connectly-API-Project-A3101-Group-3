from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from .models import Post 
from .serializers import UserSerializer, PostSerializer  
from .permissions import IsPostAuthor


#  User List & Create View
class UserListCreate(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#  Post List & Create View
class PostListCreate(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


#  Comment List & Create View (Make sure you have a Comment model)
from .models import Comment  
from .serializers import CommentSerializer  

class CommentListCreate(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk): 
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk): 
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=204)

#  Admin-Only View
class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({"message": "This is an admin-only view"})

#  Login User View
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=401)
    return JsonResponse({"message": "Invalid request"}, status=400)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class ProtectedView(APIView):
    """
    A protected API endpoint that requires authentication.
    """
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        return Response({"message": "Authenticated successfully!", "user": request.user.username})

from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer

class PostCommentsView(generics.ListAPIView):  # Ensure this exists
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id)
    
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):  # ✅ Allows GET, PUT, DELETE
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):  # ✅ Allows GET, PUT, DELETE
    queryset = User.objects.all()
    serializer_class = UserSerializer

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import User
from .serializers import UserSerializer

class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer




