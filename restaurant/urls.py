from django.urls import path
from .views import(
    RestaurantListView, RestaurantDetailView,  RestaurantUpdateView,
    CreateRestaurantView,MenuCategoryListCreateView, MenuCategoryDetailView,
    MenuItemListCreateView, MenuItemDetailView,RestaurantDestroyView
)

urlpatterns = [
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'), 

    path('restaurants/create/', CreateRestaurantView.as_view(), name='restaurant-create'),
    path('restaurants/<int:pk>/update/', RestaurantUpdateView.as_view(), name='restaurant-update'),
    path('restaurants/<int:pk>/delete/', RestaurantDestroyView.as_view(), name='restaurant-delete'),

    path('restaurants/<int:restaurant_pk>/categories/', MenuCategoryListCreateView.as_view(), name='category-list-create'),
    path('restaurants/<int:restaurant_pk>/categories/<int:pk>/', MenuCategoryDetailView.as_view(), name='category-detail'),

    path('restaurants/<int:restaurant_pk>/categories/<int:category_pk>/items/', MenuItemListCreateView.as_view, name='item-list-create'),
    path('restaurants/<int:restaurant_pk>/categories/<int:category_pk>/items/<int:pk>/', MenuItemDetailView.as_view(), name='item-detail'),
] 