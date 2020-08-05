from django.shortcuts import render 
from django.views.generic import View
from django.http import JsonResponse
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

        print(profile)
        return JsonResponse({"message":"succes"})    



class UpdateVoterProfile(View):

    def post(self,request):
        return JsonResponse({"message":"success"})


    