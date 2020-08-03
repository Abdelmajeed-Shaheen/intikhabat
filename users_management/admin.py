from django.contrib import admin
from .models import (
                     UserProfile,Voter,
                     Candidate,ComitteeMember,
                     CommunicationOfficer,
                     CampaignAdminstrator,
                     CustomComitteePermission,
                     CustomMembersPermissions,
                     CustomReportsPermissions,
                     CustomVoterssPermissions
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


@admin.register(CustomComitteePermission)
class AdminCustomComitteePermission(admin.ModelAdmin):
    list_display=['name','user']


@admin.register(CustomMembersPermissions)
class AdminCustomMembersPermissions(admin.ModelAdmin):
    list_display=['name','user']


@admin.register(CustomReportsPermissions)
class AdminCustomReportsPermissions(admin.ModelAdmin):
    list_display=['name','user']

@admin.register(CustomVoterssPermissions)
class AdminCustomVoterssPermissions(admin.ModelAdmin):
    list_display=['name','user']




