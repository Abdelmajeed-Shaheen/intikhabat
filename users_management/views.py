from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View,DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.db.utils import IntegrityError
from django.urls import reverse
from users_management.models import (UserProfile,ComitteeMember, 
                                     CampaignAdminstrator,CommunicationOfficer)
from common.models import Address
from users_management.forms import SignUpForm
from adminstration.models import Comittee
import json
from datetime import date

class LoginView(View):
    """
    Class responsible for handling for login page
    """

    def post(self, request):
        """
        Handles http post request for login page
        """
        response={}
        username=request.POST.get('username')
        password=request.POST.get('password')

        if UserProfile.objects.filter(mobile_number=username).exists():
            username=UserProfile.objects.get(mobile_number=username).user.username

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            if user.is_active:
                if hasattr(user.userprofile, 'candidate'):

                    response['redirect_to']=reverse('main')

                elif hasattr(user.userprofile, 'voter'):
                    response['redirect_to']=reverse('voter-profile',kwargs={'pk':user.userprofile.id})


                login(request, user)
                return JsonResponse(response)

            else:
                response["error"]="unauthorized access"
                return JsonResponse(response)
        else:
            
            response["error"]="invalid username or password"
            return JsonResponse(response)

                
class UserProfileView(DetailView):
    model=UserProfile
    template_name='candidate_profile.html'
    context_object_name="candidate"
    def get(self,request,pk):
        candidate=self.get_object()

        context={
            "candidate":candidate
        }
        if str(self.request.user.id) == str(candidate.user.id):
            return render(request,"candidate_profile.html",context)
        
        return HttpResponse("not found")

class CreateUser(View):

    def post(self,request):
        form=SignUpForm(request.POST)
        first_name=form.data.get('first_name')
        third_name=form.data.get('third_name')
        middle_name=form.data.get('middle_name')
        last_name=form.data.get('last_name')
        mobile_number=form.data.get('mobile_number')
        whatsapp_number=form.data.get('whatsapp_number')
        email=form.data.get('email')
        is_manager=form.data.get('first_name')
        password='changeme12'
        user_type=request.POST.get('usertype')
      
        user_instance={
            'username':mobile_number,
            'first_name':first_name,
            'last_name':last_name,
            'email':email
        }
        # try:
        user=User(**user_instance)
        user.set_password(password)
        user.save()
        # except (IntegrityError):
        #     return JsonResponse({'error':'اسم مكرر'})
        profile_instance={
            'middle_name':middle_name,
            'user':user,
            'mobile_number':mobile_number,
            'whatsapp_number':whatsapp_number,
            'date_of_birth':date.today()
            
        }
        try:
            user_profile=UserProfile(**profile_instance)
            user_profile.save()
        except (IntegrityError):
            return JsonResponse({'error':'رقم هاتف مكرر'})
        candidate=request.user.userprofile.candidate
        comittee=Comittee.objects.get(candidate=candidate)
        if user_type == "cm":
            comittee_member=ComitteeMember(profile=user_profile,candidate=request.user.userprofile.candidate,comittee=comittee)
            comittee_member.save()

        elif user_type =="camp":
            campaign_manager=CampaignAdminstrator(profile=user_profile,candidate=candidate)
            campaign_manager.save()
        
        elif user_type =="cmo":
            communication_officer=CommunicationOfficer(profile=user_profile,comittee=comittee)
            communication_officer.save()


        return JsonResponse({'message':'تم التسجيل بنجاح'})


      
class UpdateProfile(View):

    def post(self,request):
        userprofile=request.POST.get("user")
        userprofile=json.loads(userprofile)
        profile=UserProfile.objects.filter(id=int(userprofile['id']))
        User.objects.filter(id=request.user.id).update(first_name=userprofile["first_name"],last_name=userprofile["last_name"])
        
        userobject={
            'middle_name':userprofile['second_name'],
            'last_name':userprofile['third_name'],
            'mobile_number':userprofile['mobile_number'],
            'whatsapp_number':userprofile['whatsapp_number'],
            # 'address':Address.objects.get(id=int(userprofile['address']))
        }
        
        profile.update(**userobject)
        
        return JsonResponse({"user":"success"})
        




   

        