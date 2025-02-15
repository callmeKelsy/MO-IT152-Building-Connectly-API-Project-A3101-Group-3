from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import (
    UserListCreate, PostListCreate, CommentListCreate,
    login_user, PostDetailView, AdminOnlyView, ProtectedView
)

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list'),
    path('posts/', PostListCreate.as_view(), name='post-list'),
    path('comments/', CommentListCreate.as_view(), name='comment-list'),
    path('login/', obtain_auth_token, name='login-user'),
    path("admin-view/", AdminOnlyView.as_view(), name="admin-only"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("protected/", ProtectedView.as_view(), name="protected-view"),
]
