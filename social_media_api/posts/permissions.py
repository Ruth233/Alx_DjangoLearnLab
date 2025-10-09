from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners to edit or delete their objects.
    Assumes the model instance has an `author` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in SAFE_METHODS:
            return True
        # Write permissions only to the author
        return getattr(obj, 'author', None) == request.user
