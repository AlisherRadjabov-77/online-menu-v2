from django.db import models
from django.conf import settings

class Restaurant(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='owned_restaurants',
        limit_choices_to={'profile__role': 'RESTAURANTADMIN'}
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='restaurants/logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    order = models.IntegerField(default=0, help_text="Kategoriya tartibi")
    is_active = models.BooleanField(default=True)


    class Meta:
        ordering = ['order', 'id']
        unique_together = ['restaurant', 'name']

    def __str__(self) -> str:
        return f"{self.restaurant.name} - {self.name}"


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu/items/', blank=True, null=True)
    categories = models.ManyToManyField(
        MenuCategory,
        related_name='items',
        blank=True,
        help_text="Ovqat bir necha kategoriyaga kirishi mumkin"
    )
    is_available = models.BooleanField(default=True)
    preparation_time = models.IntegerField(
        default=15,
        help_text="Tayyorlanish vaqti (daqiqa)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

        def __str__(self) -> str:
            return f"{self.category.name}" - {"self.name"}


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[
            ('SUPERADMIN', 'SuperAdmin'),
            ('RESTAURANTADMIN', 'RestaurantAdmin'),
        ],
        default='RESTAURANTADMIN'
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"