from django.shortcuts import render
from django.views.generic import View,DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse
from users_management.models import UserProfile,ComitteeMember
from users_management.forms import SignUpForm
import json


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
        third_name=form.data.get('first_name')
        middle_name=form.data.get('first_name')
        last_name=form.data.get('first_name')
        mobile_number=form.data.get('first_name')
        whatsapp_number=form.data.get('first_name')
        email=form.data.get('first_name')
        is_manager=form.data.get('first_name')
        password='changeme12'
        
        

        return JsonResponse({'message':'success'})


      

        




   

        