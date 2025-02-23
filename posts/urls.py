from django.urls import path
from .views import (
    UserListCreate, UserDetailView, PostListCreate, PostDetailView, CreatePostView,
    CommentListCreate, CommentDetailView, PostCommentsView,
    login_user, AdminOnlyView, ProtectedView

)

urlpatterns = [
    # ✅ User Endpoints
    path('users/', UserListCreate.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),  

    # ✅ Post Endpoints
    path('posts/', PostListCreate.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('posts/create/', CreatePostView.as_view(), name='create-post'),  # Separate route for creating posts

    # ✅ Comment Endpoints
    path('comments/', CommentListCreate.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('posts/<int:pk>/comments/', PostCommentsView.as_view(), name='post-comments'),  


    # ✅ Authentication & Protected Routes
    path('login/', login_user, name='login-user'),  
    path("admin-view/", AdminOnlyView.as_view(), name="admin-only"),
    path("protected/", ProtectedView.as_view(), name="protected-view"),
    
    
]
