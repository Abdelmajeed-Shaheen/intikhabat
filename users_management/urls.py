from django.urls import path,re_path
from .views import LoginView,UserProfileView

urlpatterns = [
    path("user-login/",LoginView.as_view(),name="userlogin"),
    path("user-profile/<pk>/",UserProfileView.as_view(),name="user-profile")
]
