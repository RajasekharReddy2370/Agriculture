from django.urls import path
from .views import home

urlpatterns = [
    path('h/', home, name='home-h'),
]
