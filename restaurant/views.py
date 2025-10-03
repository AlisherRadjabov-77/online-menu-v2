from django.shortcuts import get_object_or_404
from .models import Restaurant, MenuCategory, MenuItem
from rest_framework import generics, permissions
from .permissions import IsRestaurantAdmin, IsSuperAdmin
from .serializers import(
    ProfileSerializer, MenuItemSerializer, MenuCategorySerializer,
    RestaurantSerializer, CreateRestaurantSerializer, UpdateRestaurantSerializer, RestaurantListSerializer
)
from rest_framework.generics import(
    ListAPIView, CreateAPIView, RetrieveAPIView, ListCreateAPIView, UpdateAPIView,DestroyAPIView
)

class RestaurantListView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer
    permission_classes = [permissions.AllowAny]

class RestaurantDetailView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]

class CreateRestaurantView(CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = CreateRestaurantSerializer
    permission_classes = [IsSuperAdmin]

class RestaurantUpdateView(UpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = UpdateRestaurantSerializer
    permission_classes = [IsRestaurantAdmin]
    lookup_field = 'pk'

    def get_queryset(self):
        return self.request.user.profile.restaurant_set.all()

class RestaurantDestroyView(DestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurantAdmin]
    lookup_field = 'pk'
    
    def get_queryset(self):
        #Faqat joriy foydalanuvchi (owner)ga tegishli restoranlarni qaytaradi
        return self.request.user.profile.restaurant_set.all()
    
class MenuCategoryListCreateView(ListCreateAPIView):
    serializer_class = MenuCategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny]
        return[IsRestaurantAdmin()]
    
    def get_queryset(self):
        return MenuItem.objects.filter(category_id=self.kwargs['category_pk'], categories__restaurant=self.kwargs["restaurant_pk"])
    
    def perform_create(self, serializer):
        category = MenuCategory.objects.get(pk=self.kwargs['category_pk'])
        serializer.save(category=category)

class MenuItemDetailView(RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.AllowAny]

class MenuCategoryDetailView(RetrieveAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer
    permission_classes = [permissions.AllowAny]

class MenuItemListCreateView(ListCreateAPIView):
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsRestaurantAdmin()]

    def get_queryset(self):
        return MenuItem.objects.filter(category_id=self.kwargs['category_pk'])

    def perform_create(self, serializer):
        category = MenuCategory.objects.get(pk=self.kwargs['category_pk'])
        serializer.save(category=category)