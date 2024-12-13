from rest_framework.permissions import BasePermission


class IsAnonUser(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_anonymous
        return False


class IsAuthorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated or user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user.is_staff
