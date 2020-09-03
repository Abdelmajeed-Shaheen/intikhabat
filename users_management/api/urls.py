from django.urls import include, path
from rest_framework import routers
from .viewset import UserProfileViewSet,GetCredsViewSet
from rest_framework_simplejwt import views as jwt_views
router = routers.DefaultRouter()

router.register(r'user', UserProfileViewSet,basename="users")



urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login',GetCredsViewSet.as_view(),name='get-creds')
]