from django.urls import path
from .views import register_request
urlpatterns = [
    # path("", views.homepage, name="homepage"),
    path("register", register_request, name="register"),

]
