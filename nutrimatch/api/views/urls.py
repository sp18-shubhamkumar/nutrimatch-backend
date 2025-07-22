from django.urls import path
from . import RegisterView, LoginView, RestaurantsOperationView, EmployeeManagementView


urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('restaurants/', RestaurantsOperationView.as_view(), name='restaurants'),
    path('restaurants/<int:rid>/',
         RestaurantsOperationView.as_view(), name='restaurants'),

    path('restaurants/<int:rid>/employees/',
         EmployeeManagementView.as_view(), name='employees'),
    path('restaurants/<int:rid>/employees/<int:eid>/',
         EmployeeManagementView.as_view(), name='employees'),

]
