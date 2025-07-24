from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRestaurantAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'restaurant_admin'
    
class IsRestaurantAdminOrEmployee(BasePermission):
    def has_object_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['restaurant_admin', 'employee']

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_superuser
    