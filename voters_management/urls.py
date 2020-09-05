from django.urls import path,re_path
from .views import CreateVoter,VoterProfile,UpdateVoter,GetCandidates,ChangeVotingStatus
urlpatterns = [
    path('create-voter/',CreateVoter.as_view(),name="create-voter"),
    re_path(r'^(?P<pk>[0-9]+)/$',VoterProfile.as_view(),name="voter-profile"),
    path("edit-voting-status/",UpdateVoter.as_view(),name="edit-voting-status"),
    path("get_candidates/",GetCandidates.as_view(),name="get_candidates"),
    path('change-voting-status',ChangeVotingStatus.as_view(),name="change-voting-status")

]
