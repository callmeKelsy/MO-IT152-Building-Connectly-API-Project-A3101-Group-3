from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserListCreate, UserDetailView, PostListCreate, CommentListCreate, CommentDetailView,
    login_user, PostDetailView, AdminOnlyView, ProtectedView, PostCommentsView
)

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),  
    path('posts/', PostListCreate.as_view(), name='post-list'),
    path('comments/', CommentListCreate.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('login/', obtain_auth_token, name='login-user'),
    path("admin-view/", AdminOnlyView.as_view(), name="admin-only"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("protected/", ProtectedView.as_view(), name="protected-view"),
    path('posts/<int:pk>/comments/', PostCommentsView.as_view(), name='post-comments'), 
]
