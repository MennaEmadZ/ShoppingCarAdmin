from django.urls import path
from .views import product_details
urlpatterns = [
    path('details/<int:product_id>', product_details, name="detail"),
]
