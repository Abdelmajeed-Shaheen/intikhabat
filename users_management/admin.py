from django.contrib import admin
from .models import (
                     UserProfile,Voter,
                     Candidate,ComitteeMember,
                     CommunicationOfficer,
                     CampaignAdminstrator
                     )

@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    list_display=['user','mobile_number','gender']


@admin.register(Voter)
class AdminVoter(admin.ModelAdmin):
    list_display=['profile','vote_status','followed_up','identiefier']


@admin.register(Candidate)
class AdminCandidate(admin.ModelAdmin):
    list_display=['profile','election_list']

@admin.register(ComitteeMember)
class AdminComitteeMember(admin.ModelAdmin):
    list_display=['profile','comittee','is_manager','candidate']



@admin.register(CommunicationOfficer)
class AdminCommunicationOfficer(admin.ModelAdmin):
    list_display=['profile','comittee']

@admin.register(CampaignAdminstrator)
class AdminCampaignAdminstrator(admin.ModelAdmin):
    list_display=['profile','candidate']


