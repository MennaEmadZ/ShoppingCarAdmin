from django.urls import path
from .views import register_request, logout_view, login_request

urlpatterns = [
    # path("", views.homepage, name="homepage"),
    path("register", register_request, name="register"),
    path("login", login_request, name="login"),
    path('logout', logout_view),
]
