from django.db import models
from django.contrib.auth.models import User
from common.models import Address,ElectionAddress
# from adminstration.models import (Comittee,ElectionList
                                
#                                 )


GENDER_CHOICES=[
                ('Male','Male'),
                ('Female','Female')
                ]

VOTE_STATUS_CHOICES=[
                ('Voting','Voting'),
                ('Not_sure','Not sure'),
                ('Not_voting','Not voting')
                ]


class UserProfile(models.Model):

    """ class representing all users profiles """
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    middle_name=models.CharField(max_length=16)
    last_name=models.CharField(max_length=16)
    mobile_number=models.CharField(max_length=14,unique=True)
    whatsapp_number=models.CharField(max_length=14,unique=True,null=True,blank=True)
    gender=models.CharField(choices=GENDER_CHOICES, max_length=50)
    date_of_birth=models.DateField()
    timestamp=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated=models.DateTimeField(auto_now=False,auto_now_add=True)
    address=models.ForeignKey(Address,on_delete=models.CASCADE,null=True,blank=True)
    work_field=models.ForeignKey('WorkField',on_delete=models.CASCADE,null=True,blank=True)
    name_string=models.CharField(max_length=255,null=True,unique=True)
        
    def __str__(self):
        return self.user.username



class Voter(models.Model):

    profile=models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    vote_status=models.CharField(choices=VOTE_STATUS_CHOICES,max_length=50,null=True)
    is_identifier=models.BooleanField(default=False)
    followed_up=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated=models.DateTimeField(auto_now=False,auto_now_add=True)
    identiefier=models.ForeignKey('Voter',on_delete=models.CASCADE,null=True,blank=True)
    voting_id=models.CharField(max_length=50,null=True,blank=True)
    candidate=models.ForeignKey("Candidate",on_delete=models.CASCADE,null=True,blank=True)
    has_elc_card=models.BooleanField(default=False)
    related_comittee_member=models.ForeignKey('ComitteeMember',on_delete=models.CASCADE,null=True,blank=True)
    election_address=models.ForeignKey(ElectionAddress,on_delete=models.CASCADE,null=True,blank=True)
    has_identifier=models.BooleanField(null=True, blank=True)
    first_login=models.BooleanField(default=True)
    def __str__(self):
        return (self.profile.user.first_name +" "+self.profile.user.last_name)

        
class Candidate(models.Model):
    
    profile=models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated=models.DateTimeField(auto_now=False,auto_now_add=True)
    election_list=models.ForeignKey(to='adminstration.ElectionList',on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=255,blank=True,null=True)
    profile_picture=models.ImageField(upload_to="candidate_images", null=True,blank=True)
    class Meta:
        permissions = [
            ("create_commitee", "Can create commitee"),
            ("add_committee_member", "can add commitee member"),
        ]
    

    def __str__(self):
        return self.profile.user.username

class CampaignAdminstrator(models.Model):

    profile=models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    candidate=models.ForeignKey('Candidate',on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated=models.DateTimeField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return (self.profile.user.first_name +" "+ self.profile.user.last_name)

class ComitteeMember(models.Model):

    profile=models.OneToOneField(UserProfile, on_delete=models.CASCADE)    
    candidate=models.ForeignKey('Candidate',on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated=models.DateTimeField(auto_now=False,auto_now_add=True)
    description=models.TextField(null=True,blank=True)
    notes=models.TextField(null=True,blank=True)
    is_manager=models.BooleanField(default=False)
    comittee=models.ForeignKey(to='adminstration.Comittee',on_delete=models.CASCADE)
    election_address=models.ForeignKey(ElectionAddress, on_delete=models.CASCADE,null=True,blank=True)
    is_active=models.BooleanField(default=False)
    def __str__(self):
        return self.profile.user.username

    
class CommunicationOfficer(models.Model):
    profile=models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    comittee=models.OneToOneField(to='adminstration.Comittee',on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username

class CustomComitteePermission(models.Model):
    can_view_comittee=models.BooleanField()
    can_update_comittee=models.BooleanField()
    can_create_comittee=models.BooleanField()
    can_remove_comittee=models.BooleanField()
    name='manage comittee'
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class CustomMembersPermissions(models.Model):
    can_view_member=models.BooleanField()
    can_update_member=models.BooleanField()
    can_create_member=models.BooleanField()
    can_remove_member=models.BooleanField()
    name='manage members'
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CustomReportsPermissions(models.Model):
    can_view_report=models.BooleanField()
    can_update_report=models.BooleanField()
    can_create_report=models.BooleanField()
    can_remove_report=models.BooleanField()
    name='manage reports'
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class CustomVoterssPermissions(models.Model):
    can_view_voter=models.BooleanField()
    can_update_voter=models.BooleanField()
    can_create_voter=models.BooleanField()
    can_remove_voter=models.BooleanField()
    name='manage voters'
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WorkField(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name
