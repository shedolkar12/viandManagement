from django.shortcuts import render

# Create your views here.

from django.urls import path
from . import views

urlpatterns = [
    path('validate_location/', views.validate_location),
    path('categories/<int:branch_id>/', views.categories),
    path('categories/<str:category>/', views.product)
]