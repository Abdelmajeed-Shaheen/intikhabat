from django.urls import path,re_path
from .views import CreateVoter,UpdateVoterProfile,VoterProfile
urlpatterns = [
    path('create-voter/',CreateVoter.as_view(),name="create-voter"),
    path('update-voter',UpdateVoterProfile,name="update-voter"),
    re_path(r'^(?P<pk>[0-9]+)/$',VoterProfile.as_view(),name="voter-profile")
]
