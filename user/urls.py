from django.urls import path
from .views import register_request, logout_view, login_request, add_to_cart

urlpatterns = [
    path("register", register_request, name="register"),
    path("login", login_request, name="login"),
    path('logout', logout_view),
    path('add-to-cart/<int:product>', add_to_cart, name='add-to-cart'),
]
