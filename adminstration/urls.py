from django.urls import path
from .views import CampaignManagementMainView,CreateComitteeView
urlpatterns = [
    path("main",CampaignManagementMainView.as_view(),name="main"),
    path("create-comittee",CreateComitteeView.as_view(),name="create-comittee")
]
