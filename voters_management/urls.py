from django.urls import path,re_path
from .views import CreateVoter,VoterProfile,UpdateVoter
urlpatterns = [
    path('create-voter/',CreateVoter.as_view(),name="create-voter"),
    re_path(r'^(?P<pk>[0-9]+)/$',VoterProfile.as_view(),name="voter-profile"),
    path("edit-voting-status/",UpdateVoter.as_view(),name="edit-voting-status")
]
