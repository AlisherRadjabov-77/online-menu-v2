from rest_framework import permissions
from .models import Restaurant, MenuCategory, MenuItem, Profile

class IsSuperAdmin(permissions.BasePermission):
    """
    SuperAdmin uchun permission: Faqat is_superuser bo'lgan userlar yangi restoran yaratishi va ro'yxatni ko'rishi mumkin.
    """
    def has_permission(self, request, view):
        # Foydalanuvchi authenticated va superuser bo'lishi kerak
        return request.user.is_authenticated and request.user.is_superuser

class IsRestaurantAdmin(permissions.BasePermission):
    """
    RestaurantAdmin uchun permission: Faqat role='RESTAURANTADMIN' bo'lgan userlar o'z restorani bilan ishlashi mumkin.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            # Profil mavjud va roli RESTAURANTADMIN bo'lishi kerak
            return request.user.profile.role == 'RESTAURANTADMIN'
        except Profile.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        # Ob'yekt (Restaurant, Category yoki Item) ning owner i request.user ga mos bo'lishi kerak
        if isinstance(obj, Restaurant):
            return obj.owner.user == request.user
        elif isinstance(obj, MenuCategory):
            return obj.restaurant.owner.user == request.user
        elif isinstance(obj, MenuItem):
            return obj.category.restaurant.owner.user == request.user
        return False