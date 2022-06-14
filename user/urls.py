from django.urls import path
from .views import register_request, logout_view

urlpatterns = [
    # path("", views.homepage, name="homepage"),
    path("register", register_request, name="register"),
    path('logout', logout_view),
]
