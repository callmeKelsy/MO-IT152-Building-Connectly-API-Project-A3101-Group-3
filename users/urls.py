from django.urls import path
from .views import UserListView, UserCreateView, UserDetailView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),  # ✅ GET /users/
    path('create/', UserCreateView.as_view(), name='user-create'),  # ✅ POST /users/create/
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # ✅ GET /users/1/
]
