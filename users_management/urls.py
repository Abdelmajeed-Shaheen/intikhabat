from django.urls import path
from .views import LoginView

urlpatterns = [
    path("user-login/",LoginView.as_view(),name="userlogin")
]
