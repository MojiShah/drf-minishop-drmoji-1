from django.urls import path
from . import views

urlpatterns = [
    path('category/',views.getCategory,name="category"),
    path('product/',views.getProduct,name="product")
]