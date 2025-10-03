from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Restaurant, MenuCategory, MenuItem, Profile
from django.core.files.base import ContentFile
import base64


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = Profile
        fields = ['user', 'role']
        read_only_fields = ['user', 'role']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image', 'category', 'is_available', 'preparation_time', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

        def validate_category(self, value):
            request = self.context.get('request')
#-----------LOGIN qilmagan userlar uchun validatsiya kerak emas (faqat ko'rish)--------------
            if not request or not request.user.is_authenticated:
                return value
#----Profil yoq oddiy userga validatsiya kerak emas----
            try:
                profile = request.user.profile
            except Profile.DoesNotExist:
                return value
                

            if profile.role=="RESTAURANTADMIN":
# ----------Restaurant Admin faqat o'z restorani uchun kategoriya ishlatishi mumkin----------
                if value.restaurant.owner.user!=request.user:
                    raise serializers.ValidationError(
                        "Bu kategoriya sizning restoraningizga tegishli emas."
                    )
            return value

class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)
    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'restaurant', 'order', 'is_active', 'items']
        read_only_fields = ['id', 'restaurant']


class RestaurantSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(read_only=True)
    #categories = MenuCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'owner', 'name', 'description', 'address', 'phone_number', 'logo', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

class UpdateRestaurantSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Restaurant
        fields = ['name', 'password'] # faqat nom va parol maydonlari
    def update(self, instance, validated_data):
        # Nomni ozgartirish
        instance.name = validated_data.get('name', instance.name)
        # Parolni ozgartirish (agar berilgan bo'lsa)
        password = validated_data.pop('password', None)
        if password:
            # Owner foydalanuvchisining parolini xavfsiz o'zgartirish (hash qilish)
            instance.owner.user.set_password(password)
            instance.owner.user.save()

            instance.save()
            return instance


class CreateRestaurantSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    logo = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Restaurant
        fields = ['name', 'logo', 'owner_username', 'password']

    def validate(self, attrs):
        User = get_user_model()
        username = attrs.get("owner_username")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                "owner_username": "Bu username allaqachon mavjud. Iltimos boshqa username tanlang"
            })
        return attrs

    def create(self, validated_data):
        User = get_user_model()

        username = validated_data.pop('owner_username')
        password = validated_data.pop('password')

        # user, created = User.objects.get_or_create(username=username)
        # if created:
        #     user.set_password(password)
        #     user.save()

        new_admin, created = User.objects.get_or_create(
            username=username,
            defaults={"password": password}
        )
        if not created:
            raise serializers.ValidationError({
                "owner_username": "Bu username allaqachon mavjud."
            })
        else:
            new_admin.set_password(password)
            new_admin.save()
        
        Profile.objects.create(user=new_admin, role='RESTAURANTADMIN')
        logo_data = validated_data.pop("logo", None)
        logo_file = None
        if logo_data and logo_data.startswith("data:image"):
            format, imgstr = logo_data.split(";base64,")
            ext = format.split("/")[-1]
            logo_file = ContentFile(base64.b64decode(imgstr), name=f"logo.{ext}")

        # restoran yaratish
        restaurant = Restaurant.objects.create(
            owner=new_admin,
            logo=logo_file,
            **validated_data
        )

        return restaurant

class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'owner', 'name', 'description', 'address', 'phone_number', 'logo', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']