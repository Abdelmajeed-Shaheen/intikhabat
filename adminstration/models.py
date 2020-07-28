from django.db import models
from common.models import Address
# from users_management.models import (ComitteeMember,Candidate,
#                                      Voter,CommunicationOfficer

#                                      )



class Comittee(models.Model):

    name=models.CharField(max_length=255)
    manager=models.OneToOneField(to='users_management.ComitteeMember',on_delete=models.CASCADE,related_name='comittee_manager')
    candidate=models.OneToOneField(to='users_management.Candidate',on_delete=models.CASCADE,related_name='comittee_candidate')
    description=models.TextField()
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now=True, auto_now_add=False)
    updated=models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

class ElectionList(models.Model):

    name=name=models.CharField(max_length=255)
    description=models.TextField()
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
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

