from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView


User = get_user_model()

# ✅ GET `/users/` (List Users)
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# ✅ POST `/users/create/` (Create User)
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# ✅ GET `/users/1/` & PUT `/users/1/` & DELETE `/users/1/`
class UserDetailView(RetrieveUpdateDestroyAPIView):  # 🔄 Allows GET, PUT, PATCH, DELETE
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
