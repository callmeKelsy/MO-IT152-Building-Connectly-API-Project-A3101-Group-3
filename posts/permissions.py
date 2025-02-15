from rest_framework import permissions

class IsPostAuthor(permissions.BasePermission):
    """
    Custom permission to only allow post authors to view/edit their posts.
    """
    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author == request.user or request.user.is_staff
