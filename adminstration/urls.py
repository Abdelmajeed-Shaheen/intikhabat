from django.urls import path
from .views import (
                    CampaignManagementMainView,CreateComitteeView,
                    GrantPermissions
                    )
urlpatterns = [
    path("main",CampaignManagementMainView.as_view(),name="main"),
    path("create-comittee",CreateComitteeView.as_view(),name="create-comittee"),
    path("grant-permession",GrantPermissions.as_view(),name="grant-permession")
]
