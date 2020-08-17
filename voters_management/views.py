from django.shortcuts import render 
from django.views.generic import View,DetailView
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from users_management.models import Voter,UserProfile,Candidate,WorkField
from adminstration.models import ElectionCard
from common.models import Address,Governorate,Department,Area
import json

class CreateVoter(View):

    def post(self,request):
        voter=json.loads(request.POST.get("voter"))

        user_object={
            "first_name":voter['first_name'],
            "last_name":voter['last_name'],
            "username":(voter['first_name']+voter['last_name']),
            "email":voter['email'],
        }
        response={}
        user=User(**user_object)
        user.set_password(voter['pwd'])
        user.save()
        voter_work=WorkField.objects.get(id=int(voter['work']))
        name_string=(voter['first_name']+voter['second_name']+voter['third_name']+voter['last_name'])

        identifier_string_list=list("0/0/0/0/0")
        
        if "identifier" in voter and voter["identifier"] not in [None,""]:
            identifier=voter['identifier']
            
            if str.isnumeric(identifier):
                identifier=list(identifier)
                identifier_string_list[0]=identifier[0]
                identifier_string_list[2]=identifier[1]
                identifier_string_list[4]=identifier[2]
                identifier_string_list[6]=identifier[3]
                identifier_string_list[8]=identifier[4]
                identifier="".join(identifier_string_list)
                identifier=Voter.objects.get(voting_id=identifier)
                print(identifier)
            else:
                
                identifier=Voter.objects.get(voting_id=identifier)
                print(identifier)

        else:
            identifier=None

       

        profile_object={
            "mobile_number":voter['mobile_number'],
            "middle_name":voter['second_name'],
            "last_name":voter['third_name'],
            "date_of_birth":voter['dob'],
            "gender":voter["gender"],
            "work_field":voter_work,
            "user":user,
            "name_string":name_string,
        }



        profile=UserProfile(**profile_object)
        profile.save()
        voter=Voter(profile=profile,identiefier=identifier)
        voter.save()
        login(request,user)
        response['redirect_to']=reverse('voter-profile',kwargs={'pk':user.userprofile.id})
        return JsonResponse(response)   


class VoterProfile(DetailView):

    model=UserProfile
    template_name='voter_profile.html'
    context_object_name="voter"
    
    def get(self,request,pk):
        voter=self.get_object()
        addresses_list=Address.objects.all()
        candidates_list=Candidate.objects.all()

        if voter.voter.candidate is not None:

            candidates_list=candidates_list.exclude(id=voter.voter.candidate.id)
      
        context={
            "voter":voter,
            "addresses_list":addresses_list,
            "candidates_list":candidates_list
           
        }
        if str(self.request.user.id) == str(voter.user.id):
            return render(request,"voter_profile.html",context)
        
        return HttpResponse("not found")

class UpdateVoter(View):

    def post(self,request):
        
        voter_object={}
        voting_id_string=list("0/0/0/0/0")
        if request.POST.get('voter_id'):
            voter_id=request.POST.get('voter_id')
            voter=Voter.objects.filter(id=int(voter_id))

        if voter.values('voting_id')[0]['voting_id'] is not None:
            voting_id=voter.values('voting_id')
            voting_id_string=list(voting_id[0]['voting_id'])
            

            
        if request.POST.get('candidate'):
            candidate=Candidate.objects.get(id=request.POST.get('candidate'))
            voter_object['candidate']=candidate
            candidate_id_string=str(candidate.id)
            candidate_address_id_string=str(candidate.profile.address.governorate.id)
            candidate_dept_id_string=str(candidate.profile.address.district.id)
            voting_id_string[2]=candidate_id_string
            voting_id_string[4]=candidate_address_id_string
            voting_id_string[6]=candidate_dept_id_string
            
            if len(voting_id_string)<7:
                voting_id_string.append(str("+"+voter.values('id')[0]['id']))

            else:
                voting_id_string[8]=str(voter.values('id')[0]['id'])


            new_id="".join(voting_id_string)
            print(new_id)
            voter_object['voting_id']=new_id
      
        if request.POST.get("status"):
            voter_object['vote_status']=request.POST.get("status")

            if request.POST.get("status") == "Not_voting":
                status_id="0"

            elif request.POST.get("status") == "Not_sure":
                status_id="1"

            else:
                status_id="3"
            
            voting_id_string[0]=status_id
            new_id="".join(voting_id_string)
            voter_object['voting_id']=new_id

        voter.update(**voter_object)

        return JsonResponse({"message":"success"})


