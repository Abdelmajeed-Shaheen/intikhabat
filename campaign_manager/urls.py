from django.contrib import admin
from django.urls import path,include
from common.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home,name='home'),
    path("user-management/",include('users_management.urls')),
    path("campaign-management/",include('adminstration.urls')),
    path("voter-management/",include("voters_management.urls"))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
