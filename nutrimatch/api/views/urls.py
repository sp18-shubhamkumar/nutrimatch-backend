from django.urls import path
from . import RegisterView, LoginView, RestaurantsOperationView, EmployeeManagementView, FoodItemView, IngredientsView


urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('restaurants/', RestaurantsOperationView.as_view(), name='restaurants'),
    path('restaurants/<int:rid>/',
         RestaurantsOperationView.as_view(), name='restaurant-details'),

    path('restaurants/<int:rid>/employees/',
         EmployeeManagementView.as_view(), name='employees'),
    path('restaurants/<int:rid>/employees/<int:eid>/',
         EmployeeManagementView.as_view(), name='employee-details'),

    path('restaurants/<int:rid>/food-items/',
         FoodItemView.as_view(), name='food-items'),
    path('restaurants/<int:rid>/food-items/<int:fid>/',
         FoodItemView.as_view(), name='food-item-details'),

    path('ingredients/',
         IngredientsView.as_view(), name='ingredients'),
    path('ingredients/<int:iid>/',
         IngredientsView.as_view(), name='ingredient-detail'),

]
