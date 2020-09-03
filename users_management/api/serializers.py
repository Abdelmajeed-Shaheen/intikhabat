from rest_framework import serializers
from users_management.models import (
                                    UserProfile,Voter,
                                    ComitteeMember,CampaignAdminstrator,
                                    Candidate
                                    )
from common.models import ElectionAddress,Governorate,Department

from adminstration.models import Comittee
from django.contrib.auth.models import User




class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=["id","username","first_name","last_name","email"]



class GoverornorateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Governorate
        fields=['name']

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Department
        fields=['name']

class ElectionAddressSerializer(serializers.ModelSerializer):
    governorate=GoverornorateSerializer()
    department=DepartmentSerializer()

    class Meta:
        model=ElectionAddress
        fields=["governorate","department"]





class UserProfileSerializer(serializers.ModelSerializer):
    user=LoginSerializer()
    class Meta:
        model=UserProfile
        fields=["user","middle_name","last_name","mobile_number","whatsapp_number","gender"]


class CandidateSerializer(serializers.ModelSerializer):
    profile=UserProfileSerializer()
    class Meta:
        model=Candidate
        fields=['profile','title']


class ComitteeSerializer(serializers.ModelSerializer):
    candidate=CandidateSerializer()
    class Meta:
        model=Comittee
        fields=['candidate']

# class CommitteeMemberSerializer(serializers.ModelSerializer):
#     profile=UserProfileSerializer()
#     candidate=CandidateSerializer()
#     comittee=


class VoterSerializer(serializers.ModelSerializer):
    
    profile=UserProfileSerializer()
    election_address=ElectionAddressSerializer()
    candidate=serializers.SerializerMethodField()
    related_comittee_member=serializers.SerializerMethodField()
    identiefier=serializers.SerializerMethodField()
    user_type=serializers.SerializerMethodField()
    class Meta:
        model = Voter
        fields = ['id', 'profile','candidate',"election_address","related_comittee_member","identiefier","user_type"]

    def get_candidate(self,obj):
        candidate=Candidate.objects.get(id=int(obj.id))
        candidate_name=(candidate.profile.user.first_name +" " +candidate.profile.user.last_name)
        candidate_id=candidate.id
        candidate_object={}
        candidate_object['name']=candidate_name
        candidate_object["id"]=candidate_id
        candidate_object["election_list"]=candidate.election_list.name

        return candidate_object


    def get_related_comittee_member(self,obj):
        commitee_member=ComitteeMember.objects.get(id=int(obj.id))
        commitee_member_name=(commitee_member.profile.user.first_name +" " +commitee_member.profile.user.last_name)
        commitee_member_id=commitee_member.id
        commitee_member_object={}
        commitee_member_object['name']=commitee_member_name
        commitee_member_object["id"]=commitee_member_id

        return commitee_member_object
    
    def get_identiefier(self,obj):
        identifier=Voter.objects.get(id=int(obj.id))
        identifier_object={}
        if identifier.identiefier:
            identifier_name=(identifier.identiefier.profile.user.first_name +" " +identifier.identiefier.profile.user.last_name)
            identifier_id=identifier.identiefier.id  
            identifier_object['name']=identifier_name
            identifier_object["id"]=identifier_id
        else:
            identifier_object['name']=None
            identifier_object["id"]=None            

        return identifier_object

    def get_user_type(self,obj):
        user_type="voter"
        return user_type