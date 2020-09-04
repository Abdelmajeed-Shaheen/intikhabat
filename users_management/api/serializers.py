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
        candidate=Candidate.objects.get(id=int(obj.candidate.id))
        candidate_name=(candidate.profile.user.first_name +" " +candidate.profile.user.last_name)
        candidate_id=candidate.id
        candidate_object={}
        candidate_object['name']=candidate_name
        candidate_object["id"]=candidate_id
        candidate_object["election_list"]=candidate.election_list.name

        return candidate_object


    def get_related_comittee_member(self,obj):
        commitee_member=ComitteeMember.objects.get(id=int(obj.related_comittee_member.id))
        commitee_member_name=(commitee_member.profile.user.first_name +" " +commitee_member.profile.user.last_name)
        commitee_member_id=commitee_member.id
        commitee_member_object={}
        commitee_member_object['name']=commitee_member_name
        commitee_member_object["id"]=commitee_member_id

        return commitee_member_object
    
    def get_identiefier(self,obj):
        identifier=Voter.objects.get(id=int(obj.identiefier.id))
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




class CandidateProfileSerializer(serializers.ModelSerializer):
    
    profile=UserProfileSerializer()
    election_list=serializers.SerializerMethodField()
    user_type=serializers.SerializerMethodField()
    election_list=serializers.SerializerMethodField()
    election_address=serializers.SerializerMethodField()
    comittees=serializers.SerializerMethodField()
    campaign_admin=serializers.SerializerMethodField()
    class Meta:
        model = Voter
        fields = ['id', 'profile',"election_list","user_type","election_address","comittees","campaign_admin"]

    def get_election_list(self,obj):
        election_list_object={}
        election_list_object['name']=obj.election_list.name
        return election_list_object

    def get_election_address(self,obj):
        election_address=obj.election_list.election_address
        election_address_obj={
            "governorate":election_address.governorate.name,
            "department":election_address.department.name,

        }
        return election_address_obj

    def get_user_type(self,obj):
        user_type="candidate"
        return user_type
    
    def get_comittees(self,obj):
        comittees_list=Comittee.objects.filter(candidate=obj)
        comittees_list_response=[]
        for comittee in comittees_list:
            comittee_object={}
            comittee_object["name"]=comittee.name
            comittee_object["is_active"]=comittee.is_active
            if comittee.manager:
                comittee_object["manager"]=str(comittee.manager.profile.user.first_name+" "+comittee.manager.profile.user.last_name)
            else:
                comittee_object["manager"]="لا يوجد مدير"
            comittee_object["address"]=comittee.address_description

            comittees_list_response.append(comittee_object)
        return comittees_list_response

    def get_campaign_admin(self,obj):
        campaign_admin=str(obj.campaignadminstrator.profile.user.first_name +" "+obj.campaignadminstrator.profile.user.last_name)
        campaign_admin_mobile=obj.campaignadminstrator.profile.mobile_number
        campaign_admin_email=obj.campaignadminstrator.profile.user.email
        campaign_admin={
            "campiagn_adminstrator":campaign_admin,
            "campaign_admin_mobile":campaign_admin_mobile,
            "campaign_admin_email":campaign_admin_email,
        }

        return campaign_admin



class CampaignAdminProfileSerializer(serializers.ModelSerializer):
    
    profile=UserProfileSerializer()
    election_list=serializers.SerializerMethodField()
    user_type=serializers.SerializerMethodField()
    election_list=serializers.SerializerMethodField()
    election_address=serializers.SerializerMethodField()
    comittees=serializers.SerializerMethodField()
    

    class Meta:
        model = Voter
        fields = ['id', 'profile',"election_list","user_type","election_address","comittees"]

    def get_election_list(self,obj):
        election_list_object={}
        election_list_object['name']=obj.candidate.election_list.name
        return election_list_object

    def get_election_address(self,obj):
        election_address=obj.candidate.election_list.election_address
        election_address_obj={
            "governorate":election_address.governorate.name,
            "department":election_address.department.name,

        }
        return election_address_obj

    def get_user_type(self,obj):
        user_type="campaign_admin"
        return user_type
    
    def get_comittees(self,obj):
        comittees_list=Comittee.objects.filter(candidate=obj.candidate)
        comittees_list_response=[]
        for comittee in comittees_list:
            comittee_object={}
            comittee_object["name"]=comittee.name
            comittee_object["is_active"]=comittee.is_active
            if comittee.manager:
                comittee_object["manager"]=str(comittee.manager.profile.user.first_name+" "+comittee.manager.profile.user.last_name)
            else:
                comittee_object["manager"]="لا يوجد مدير"
            comittee_object["address"]=comittee.address_description

            comittees_list_response.append(comittee_object)
        return comittees_list_response

class ComitteeMemberSerializer(serializers.ModelSerializer):
    profile=UserProfileSerializer()
    comittee=serializers.SerializerMethodField()
    campaign_admin=serializers.SerializerMethodField()
    candidate=serializers.SerializerMethodField()
    comittee_members=serializers.SerializerMethodField()
    user_type=serializers.SerializerMethodField()


    class Meta:
        model=ComitteeMember

        fields=["id","profile","candidate","campaign_admin","comittee","is_manager","comittee_members","user_type"]
    
    def get_comittee(self,obj):
        comittee=obj.comittee.name

        comittee={
            "name":comittee
        }
    
        return comittee

    def get_candidate(self,obj):
        candidate=str(obj.candidate.profile.user.first_name +" "+obj.candidate.profile.user.last_name)
        candidate={
            "name":candidate,
            "election_list":obj.candidate.election_list.name
        }

        return candidate
    
    def get_user_type(self,obj):
        usertype="comittee_member"

        return usertype
    
    def get_comittee_members(self,obj):
        comittee_members_list=ComitteeMember.objects.filter(comittee=obj.comittee)
        comittee_members_list_response=[]

        for member in comittee_members_list:
            member_object={
                "name":str(member.profile.user.first_name+" "+member.profile.user.last_name),
                "mobile_number":member.profile.mobile_number,
                "email":member.profile.user.email,
            }
            comittee_members_list_response.append(member_object)
        return comittee_members_list_response
    
    def get_campaign_admin(self,obj):
        campaign_admin=CampaignAdminstrator.objects.get(candidate=obj.candidate)

        campaign_admin={
            "name":str(campaign_admin.profile.user.first_name +" "+campaign_admin.profile.user.last_name),
            "mobile_number":campaign_admin.profile.mobile_number,
            "email":campaign_admin.profile.user.email
        }

        return campaign_admin