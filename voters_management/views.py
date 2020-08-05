from django.shortcuts import render 
from django.views.generic import View,DetailView
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User
from users_management.models import Voter,UserProfile

from common.models import Address
import json

class CreateVoter(View):

    def post(self,request):
        voter=json.loads(request.POST.get("voter"))

        user_object={
            "first_name":voter['first_name'],
            "last_name":voter['last_name'],
            "username":(voter['first_name']+voter['last_name']),
            "email":voter['email'],
            "password":voter['pwd']
        }
        
        user=User(**user_object)
        user.save()
        profile_object={
            "mobile_number":voter['mobile_number'],
            "whatsapp_number":voter['whatsapp_number'],
            "middle_name":voter['second_name'],
            "last_name":voter['third_name'],
            "date_of_birth":voter['dob'],
            "gender":voter["gender"],
            "address":Address.objects.get(id=int(voter['address'])),
            "user":user
            
        }
        profile=UserProfile(**profile_object)
        profile.save()
        voter=Voter(profile=profile)
        voter.save()
        print(voter)
        return JsonResponse({"message":"succes"})    



class UpdateVoterProfile(View):

    def post(self,request):
        return JsonResponse({"message":"success"})


class VoterProfile(DetailView):

    model=UserProfile
    template_name='voter_profile.html'
    context_object_name="voter"
    
    def get(self,request,pk):
        voter=self.get_object()
        addresses_list=Address.objects.all()
        context={
            "voter":voter,
            "addresses_list":addresses_list
        }
        if str(self.request.user.id) == str(voter.user.id):
            return render(request,"voter_profile.html",context)
        
        return HttpResponse("not found")


    