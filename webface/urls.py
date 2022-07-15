from django.urls import path
from .views import home, register, singin, cabinet, user_logout, add_search

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('singin/', singin, name='singin'),
    path('cabinet/', cabinet, name='cabinet'),
    path('logout/', user_logout, name='logout'),
    path('add_search/', add_search, name='add_search')
]
