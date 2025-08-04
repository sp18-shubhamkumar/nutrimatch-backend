from django.urls import path
from . import (RegisterView, LoginView, RestaurantsOperationView, EmployeeManagementView,
               FoodItemView, IngredientsView, IngredientRequestView, DiseaseRequestView,
               IngredientRequestApprovalView, DiseaseManagementView, CustomerProfileView,
               FoodSuggestionsView, IngredientBulkUploadView, DiseaseBulkUploadView)


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
    path('ingredients/upload/', IngredientBulkUploadView.as_view(),
         name='ingredient-bulk-upload'),

    path('requests/disease/', DiseaseRequestView.as_view(), name='disease-request'),
    path('requests/ingredients/', IngredientRequestView.as_view(),
         name='ingredient-request'),

    path('requests/ingredients/<int:pk>/',
         IngredientRequestApprovalView.as_view(), name='ingredient-request-approval'),

    path('diseases/',
         DiseaseManagementView.as_view(), name='diseases'),
    path('diseases/<int:pk>/',
         DiseaseManagementView.as_view(), name='disease-details'),
    path('diseases/upload/', DiseaseBulkUploadView.as_view(),
         name='disease-bulk-upload'),

    path('customer/profile/', CustomerProfileView.as_view(),
         name='csutomer-profile'),
    path('customer/food-suggestions/', FoodSuggestionsView.as_view(),
         name='customer-suggested-foods'),


]
