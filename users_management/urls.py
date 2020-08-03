from django.urls import path,re_path
from .views import LoginView,UserProfileView,CreateUser

urlpatterns = [
    path("user-login/",LoginView.as_view(),name="userlogin"),
    path("user-profile/<pk>/",UserProfileView.as_view(),name="user-profile"),
    path("create-user/",CreateUser.as_view(),name="create-user")
]
