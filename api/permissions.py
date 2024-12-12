from rest_framework.permissions import BasePermission


class IsAnonUser(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_anonymous
        return False
