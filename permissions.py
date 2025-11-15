from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to anyone, but write access only to admin users.
    This is suitable for public-facing data like listings and categories, where anyone can view,
    but only an admin can modify or create.
    """
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for any user.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to anyone, but write access only to the owner
    of the object. This is ideal for user-specific data like submissions, reviews, and comments.
    """
    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) for any user.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed if the user is the owner of the object.
        return obj.user == request.user

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to allow access only to admin users.
    This is used for the admin-only API endpoints.
    """
    def has_permission(self, request, view):
        # The user must be authenticated and have staff status (admin).
        return request.user and request.user.is_staff
