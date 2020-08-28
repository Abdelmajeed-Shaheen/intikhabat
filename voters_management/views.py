from django.shortcuts import render 
from django.views.generic import View,DetailView
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from users_management.models import Voter,UserProfile,Candidate,WorkField
from adminstration.models import ElectionCard,ElectionAddress,ElectionList
from common.models import Address,Governorate,Department,Area
import json
import re
import datetime



def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

def hasLetters(inputString):
    return bool(re.search(r'[a-zA-Z]', inputString))
    
class CreateVoter(View):

    def post(self,request):
        voter=json.loads(request.POST.get("voter"))
        name_string=(voter['first_name']+voter['second_name']+voter['third_name']+voter['last_name'])
        if hasNumbers(name_string):
            return JsonResponse({"error":"لايمكن للاسم ان يحتوي ارقام"})

        if hasLetters(voter['mobile_number']) :
            return JsonResponse({'error':"لا يمكن لرقم الهاتف ان يحتوي احرف"})
        try:
            user_object={
                "first_name":voter['first_name'],
                "last_name":voter['last_name'],
                "username":(voter['mobile_number']),
                "email":voter['email'],
            }

            response={}
            user=User(**user_object)

            if len(voter['pwd']) < 8 :
                return JsonResponse({"error":"كلمة السر يجب ان تكون ٨ خانات على الاقل"})
            
            if not hasNumbers(voter['pwd']):
                return JsonResponse({"error":"يجب ان تحتوي كلمة السر على ارقام"})
            
            user.set_password(voter['pwd'])
            user.save()

            if voter["work"] in ["",None]:
                return JsonResponse({"error":"حقل العمل مطلوب"})
            voter_work=WorkField.objects.get(id=int(voter['work']))

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

            print("success: ",user_object)

            election_address={}
            if 'governorate' in voter and voter['governorate'] not in [None,""]:
                governorate=Governorate.objects.get(id=int(voter['governorate']))
                election_address['governorate']=governorate

            if 'dept' in voter and voter['dept'] not in [None,""]:
                dept=Department.objects.get(id=int(voter['dept']))
                election_address['department']=dept

            if 'department' in election_address and 'governorate' in election_address:
                ea=ElectionAddress(**election_address)
                ea.save()
            voter=Voter(profile=profile,election_address=ea)
            voter.save()
            login(request,user)
            response['redirect_to']=reverse('voter-profile',kwargs={'pk':user.userprofile.id})
            return JsonResponse(response)
       
        except IntegrityError :

            if User.objects.filter(username=voter['mobile_number']).exists():
                error_message="رقم هاتف مكرر  {0}"
                error_message=error_message.format(voter['mobile_number'])
            
            if User.objects.filter(email=voter['email']).exists():
                error_message="بريد الكتروني مكرر  {0}"
                error_message=error_message.format(voter['email'])                

            if UserProfile.objects.filter(name_string=name_string).exists():
              
                error_message="هذا الناخب مسجل مسبقا"

            return JsonResponse({"error":error_message})

class VoterProfile(DetailView):

    model=UserProfile
    template_name='voter_profile.html'
    context_object_name="voter"
    
    def get(self,request,pk):
        voter=self.get_object()
        addresses_list=Address.objects.all()
        candidates_list=Candidate.objects.all()
        ea=voter.voter.election_address
        election_lists=ElectionList.objects.all().filter(election_address__department=ea.department)
        areas_list=Area.objects.all().filter(department=voter.voter.election_address.department)
        if voter.voter.candidate is not None:

            candidates_list=candidates_list.exclude(id=voter.voter.candidate.id)
     
        context={
            "voter":voter,
            "addresses_list":addresses_list,
            "candidates_list":candidates_list,
            "election_lists":election_lists,
            "areas_list":areas_list
           
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
            candidate_address_id_string=str(candidate.election_list.election_address.governorate.id)
            candidate_dept_id_string=str(candidate.election_list.election_address.department.id)
            voting_id_string[2]=candidate_id_string
            voting_id_string[4]=candidate_address_id_string
            voting_id_string[6]=candidate_dept_id_string
            
            if len(voting_id_string)<7:
                voting_id_string.append(str("+"+voter.values('id')[0]['id']))

            else:
                voting_id_string[8]=str(voter.values('id')[0]['id'])


            new_id="".join(voting_id_string)
           
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
        
        if request.POST.get('ec'):
            if request.POST.get('ec')=='true':
                voter_object['has_elc_card']=True
            else:
                voter_object['has_elc_card']=False

        if request.POST.get('has_identifier')== 'true':
            has_identifier=True
        elif request.POST.get('has_identifier')== 'false':
            has_identifier=False
        else:
            has_identifier=None

        if request.POST.get('identifier') not in [None,""]:
            identifier=request.POST.get('identifier')
            
            identifier_string_list=list("0/0/0/0/0")
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

        first_login=False

        voter_object['identiefier']=identifier
        voter_object['first_login']=first_login
        voter_object['has_identifier']=has_identifier
        voter.update(**voter_object)

        return JsonResponse({"message":"success"})


class GetCandidates(View):

    def get(self,request):
        election_list=request.GET.get('election_list')
        election_list=ElectionList.objects.get(id=int(election_list))

        candidates_list=Candidate.objects.filter(election_list=election_list)

        response=[]

        for candidate in candidates_list:
            obj={}
            obj['id']=candidate.id
            name=str(candidate.profile.user.first_name+" "+candidate.profile.user.last_name)
            if candidate.title:
                if not "(" in candidate.title:
                    title=(" ","(",candidate.title,")")
                    title="".join(title)
                else:
                    title=candidate.title
                print(name+" "+title)
                obj['name']=name+title
            else:
                obj['name']=name

            response.append(obj)
        
        return JsonResponse(response,safe=False)