from django.urls import path
from .views import (
                    CampaignManagementMainView,CreateComitteeView,
                    GrantPermissions,ComitteeMemberView
                    )
urlpatterns = [
    path("main",CampaignManagementMainView.as_view(),name="main"),
    path("comittee-member",ComitteeMemberView.as_view(),name="comittee-member"),
    path("create-comittee",CreateComitteeView.as_view(),name="create-comittee"),
    path("grant-permession",GrantPermissions.as_view(),name="grant-permession")
]
