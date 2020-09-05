from django.contrib import admin
from django.urls import path,include
from common.views import home
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title="Notes API")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home,name='home'),
    path("user-management/",include('users_management.urls')),
    path("campaign-management/",include('adminstration.urls')),
    path("voter-management/",include("voters_management.urls")),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/',include('users_management.api.urls'),name="api"),
    path('api/docs/', schema_view),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)