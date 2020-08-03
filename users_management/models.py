from django.db import models
from django.contrib.auth.models import User
from common.models import Address
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

    def __str__(self):
        return self.user.username



class Voter(models.Model):

    profile=models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    vote_status=models.CharField(choices=VOTE_STATUS_CHOICES,max_length=50)
    is_identifier=models.BooleanField(default=False)
    followed_up=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated=models.DateTimeField(auto_now=False,auto_now_add=True)
    identiefier=models.OneToOneField('Voter',on_delete=models.CASCADE,null=True)
    voting_id=models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.profile

class Candidate(models.Model):
    
    profile=models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated=models.DateTimeField(auto_now=False,auto_now_add=True)
    election_list=models.OneToOneField(to='adminstration.ElectionList',on_delete=models.CASCADE,null=True)
    
    class Meta:
        permissions = [
            ("create_commitee", "Can create commitee"),
            ("add_committee_member", "can add commitee member"),
        ]
    # profile_picture=models.ImageField(upload_to="path")

    def __str__(self):
        return self.profile.user.username

class CampaignAdminstrator(models.Model):

    profile=models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    candidate=models.ForeignKey('Candidate',on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated=models.DateTimeField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return self.profile

class ComitteeMember(models.Model):

    profile=models.OneToOneField(UserProfile, on_delete=models.CASCADE)    
    candidate=models.ForeignKey('Candidate',on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated=models.DateTimeField(auto_now=False,auto_now_add=True)
    description=models.TextField(null=True,blank=True)
    notes=models.TextField(null=True,blank=True)
    is_manager=models.BooleanField(default=False)
    comittee=models.OneToOneField(to='adminstration.Comittee',on_delete=models.CASCADE)

    def __str__(self):
        return self.profile

    
class CommunicationOfficer(models.Model):
    profile=models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    comittee=models.OneToOneField(to='adminstration.Comittee',on_delete=models.CASCADE)

    def __str__(self):
        self.profile

