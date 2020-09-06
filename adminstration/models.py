from django.db import models
from common.models import Address,ElectionAddress
from users_management.models import (ComitteeMember,Candidate,
                                      Voter,CommunicationOfficer

                                     )



class Comittee(models.Model):

    name=models.CharField(max_length=255)
    candidate=models.ForeignKey(to='users_management.Candidate',on_delete=models.CASCADE,related_name='comittee_candidate')
    description=models.TextField()
    address=models.ForeignKey(Address,on_delete=models.CASCADE,null=True,blank=True)
    is_active=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now=True, auto_now_add=False)
    updated=models.DateTimeField(auto_now=False, auto_now_add=True)
    manager=models.ForeignKey(ComitteeMember,on_delete=models.CASCADE,null=True,blank=True,related_name='comittee_manager')
    communication_comittee=models.BooleanField(default=False)
    election_box_comittee=models.BooleanField(default=False)
    address_description=models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.name

class ElectionList(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    election_address=models.ForeignKey(ElectionAddress,on_delete=models.CASCADE,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now=True, auto_now_add=False)
    updated=models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

class ElectionCard(models.Model):
    voter=models.OneToOneField(to='users_management.Voter',on_delete=models.CASCADE)
    candidate=models.OneToOneField(to='users_management.Candidate', on_delete=models.CASCADE)
    communication_officer=models.OneToOneField(to='users_management.CommunicationOfficer', on_delete=models.CASCADE)

    def __str__(self):
        return (self.voter.profile.user.first_name +" "+self.voter.profile.user.last_name)

