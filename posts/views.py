from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from .models import Post  #  Ensure Post model is imported
from .serializers import UserSerializer, PostSerializer  # ✅ Ensure serializers are imported
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
from .models import Comment  #  Ensure Comment model exists
from .serializers import CommentSerializer  #  Ensure serializer exists

class CommentListCreate(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


#  Post Detail View
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)  
        self.check_object_permissions(request, post)  
        return Response({"content": post.content})


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
    authentication_classes = [TokenAuthentication]  # Uses Token Authentication
    permission_classes = [IsAuthenticated]  # Restricts access to authenticated users only

    def get(self, request):
        return Response({"message": "Authenticated successfully!", "user": request.user.username})
