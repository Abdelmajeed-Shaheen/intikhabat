from django.shortcuts import render
from django.views.generic import View,DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.db.utils import IntegrityError
from django.urls import reverse
from users_management.models import UserProfile,ComitteeMember
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
                    login(request, user)
                    return HttpResponse("hello user: %s" %request.user)

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

        if user_type == "cm":
            candidate=request.user.userprofile.candidate
            comittee=Comittee.objects.get(candidate=candidate)
            comittee_member=ComitteeMember(profile=user_profile,candidate=request.user.userprofile.candidate,comittee=comittee)
            comittee_member.save()

            print(comittee_member)
        return JsonResponse({'message':'تم التسجيل بنجاح'})


      

        




   

        