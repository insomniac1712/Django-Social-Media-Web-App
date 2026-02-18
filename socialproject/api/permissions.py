from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnnerReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if hasattr(obj, "user"):
            return obj.user == request.user
        elif hasattr(obj, "posted_by"):
            return obj.posted_by == request.user
        return False
