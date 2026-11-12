from django.urls import path
from . import views

urlpatterns = [
    path('categories/',views.getCategories,name="categories"),
    path('category/<int:pk>',views.getCategory,name="category"),
    path('products/',views.getProducts,name="products"),
    path('product/<int:pk>',views.getProduct,name="product")
]