from django.urls import path
from .views import CreateVoter,UpdateVoterProfile
urlpatterns = [
    path('create-voter/',CreateVoter.as_view(),name="create-voter"),
    path('update-voter',UpdateVoterProfile,name="update-voter")
]
