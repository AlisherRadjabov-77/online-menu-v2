from django.contrib import admin
from .models import Profile, Restaurant, MenuCategory, MenuItem

# MenuCategory Inline (restoran ichida kategoriyalarni ko'rsatish uchun)
class MenuCategoryInline(admin.TabularInline):
    model = MenuCategory
    extra = 1
    fields = ('name', 'order', 'is_active')

# Restaurant Admin (soddalashtirildi, faqat zarur qismlar saqlangan)
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone_number', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'owner__username', 'address')
    inlines = [MenuCategoryInline]
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Umumiy ma\'lumotlar', {'fields': ('name', 'owner', 'description')}),
        ('Manzil va aloqa', {'fields': ('address', 'phone_number')}),
        ('Brend', {'fields': ('logo',)}),
        ('Status va sana', {'fields': ('is_active', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'profile') and request.user.profile.role == 'RESTAURANTADMIN':
            return qs.filter(owner=request.user)
        return qs

# MenuCategory Admin (soddalashtirildi, ManyToMany uchun inline olib tashlandi)
@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'order', 'is_active')
    list_filter = ('restaurant', 'is_active')
    search_fields = ('name', 'restaurant__name')
    list_editable = ('order', 'is_active')

    fieldsets = (
        ('Kategoriya ma\'lumotlari', {'fields': ('name', 'restaurant', 'order')}),
        ('Status', {'fields': ('is_active',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'profile') and request.user.profile.role == 'RESTAURANTADMIN':
            return qs.filter(restaurant__owner=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change and hasattr(request.user, 'profile') and request.user.profile.role == 'RESTAURANTADMIN':
            obj.restaurant = request.user.owned_restaurants.first()
        super().save_model(request, obj, form, change)

# MenuItem Admin (ManyToMany categories ga moslashtirildi, soddalashtirildi)
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'preparation_time', 'created_at')
    list_filter = ('is_available', 'categories__restaurant')
    search_fields = ('name', 'description', 'categories__name')
    list_editable = ('is_available', 'price')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Ovqat ma\'lumotlari', {'fields': ('name', 'categories', 'description', 'price')}),
        ('Rasm va holat', {'fields': ('image', 'is_available', 'preparation_time')}),
        ('Sana', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(request.user, 'profile') and request.user.profile.role == 'RESTAURANTADMIN':
            return qs.filter(categories__restaurant__owner=request.user).distinct()
        return qs

# Profile Admin (zarur bo'lsa qo'shilgan, soddalashtirildi)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)