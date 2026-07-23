from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("category/<slug:slug>/", views.category_products, name="category"),
    path("product/<slug:slug>/", views.product_detail, name="detail"),
]