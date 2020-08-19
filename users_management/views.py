from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View,DetailView
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.db.utils import IntegrityError
from django.urls import reverse
from users_management.models import (UserProfile,ComitteeMember, 
                                     CampaignAdminstrator,CommunicationOfficer)
from common.models import (Address,
                           Governorate,
                           Department,
                           Area,
                           District
                           )
from users_management.forms import SignUpForm
from adminstration.models import Comittee
from voters_management.views import UpdateVoter
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
                if hasattr(user.userprofile, 'candidate') or hasattr(user.userprofile, 'campaignadminstrator'):

                    response['redirect_to']=reverse('main')
                
                elif hasattr(user.userprofile,'comitteemember'):
                    response['redirect_to']=reverse('comittee-member')
 
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

class LogoutView(View):
    """
    Class responsible for logout
    """

    def get(self, request):
        """

        """
        logout(request)
        return HttpResponseRedirect(reverse('home'))

                
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
        is_manager=form.data.get('is_manager')
        print(is_manager)
        if is_manager =="on":
            is_manager=True
        else:
            is_manager=False
        password='changeme12'
        user_type=request.POST.get('usertype')
        comittee=""
        print(user_type)
        if request.POST.get('comittee'):
            comittee=Comittee.objects.get(id=request.POST.get('comittee'))
      
        user_instance={
            'username':mobile_number,
            'first_name':first_name,
            'last_name':last_name,
            'email':email
        }
        user=User(**user_instance)
        user.set_password(password)
        user.save()

        profile_instance={
            'middle_name':middle_name,
            'last_name':third_name,
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
        
        if hasattr(request.user.userprofile,'candidate') :
            candidate=request.user.userprofile.candidate
        
        if hasattr(request.user.userprofile,'campaignadminstrator') :
            candidate=request.user.userprofile.campaignadminstrator.candidate
    
        if hasattr(request.user.userprofile,'comitteemember') :
            candidate=request.user.userprofile.comitteemember.candidate


        if user_type == "cm":
          
            comittee_member_object={
                'profile':user_profile,
                'candidate':candidate,
                'comittee':comittee,
                'is_manager':is_manager
            }
            comittee_member=ComitteeMember(**comittee_member_object)
            comittee_member.save()

            comittee=Comittee.objects.get(id=comittee_member.comittee.id)
            comittee.manager=comittee_member
            comittee.save()
        
        if user_type == "cmo":
            print("hi")
            comittee_member_object={
                'profile':user_profile,
                'candidate':candidate,
                'comittee':comittee,
                'is_manager':False
            }
            comittee_member=ComitteeMember(**comittee_member_object)
            comittee_member.save()

            comittee=Comittee.objects.get(id=comittee_member.comittee.id)
            comittee.save()

        elif user_type =="camp":
            campaign_manager=CampaignAdminstrator(profile=user_profile,candidate=candidate)
            campaign_manager.save()


        return JsonResponse({'message':'تم التسجيل بنجاح'})


      
class UpdateProfile(View):

    def post(self,request):
        userprofile=request.POST.get("user")
        print(userprofile)
        userprofile=json.loads(userprofile)
        User.objects.filter(id=request.user.id).update(first_name=userprofile["first_name"],last_name=userprofile["last_name"])
        
        profile=UserProfile.objects.get(id=int(userprofile['id']))
        print(profile)
        user_object={}
        empty=[None,""]
       
        if 'second_name' in userprofile and userprofile['second_name'] not in empty:
            user_object['middle_name']=userprofile['second_name']
        

        if 'third_name' in userprofile and userprofile['third_name'] not in empty:
            user_object['last_name']=userprofile['third_name']
        
        if 'mobile_number' in userprofile and userprofile['mobile_number'] not in empty:
            user_object['mobile_number']=userprofile['mobile_number']
            profile.mobile_number=user_object['mobile_number']

        if 'whatsapp_number' in userprofile and userprofile['whatsapp_number'] not in empty:
            user_object['whatsapp_number']=userprofile['whatsapp_number']
            profile.whatsapp_number=user_object['whatsapp_number']
            profile.save()


        if 'district' in userprofile and userprofile['district'] not in empty:
            district=District.objects.get(id=int(userprofile['district']))
            area=district.area

            userprofile['address__district']=district
            userprofile['address__area']=area


        if 'title' in userprofile and userprofile['title'] is not None:
            candidate=request.user.userprofile.candidate
            candidate.title=userprofile['title']
            candidate.save()        

        profile.save()
        
        return JsonResponse({"user":"success"})
        




   

        