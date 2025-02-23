from rest_framework.permissions import BasePermission

class IsPostAuthor(BasePermission):
    """
    Custom permission to allow only the author of a post or an admin to edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff  
