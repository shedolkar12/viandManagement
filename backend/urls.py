from django.shortcuts import render

# Create your views here.

from django.urls import path
from . import views
# (?P<category>\w{0,50})
urlpatterns = [
    path('validate_location/', views.validate_location),
    path('categories/<int:branch_id>/', views.categories),
    path('categories/<int:branch_id>/<str:category>/', views.productList),
    path('comboproducts/<int:branch_id>/', views.comboProductsList),
    path('placeOrder/', views.placeOrder),
]