from rest_framework.permissions import BasePermission


class IsRestaurantAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'restaurant_admin'
    
class IsRestaurantAdminOrEmployee(BasePermission):
    def has_object_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['restaurant_admin', 'employee']
