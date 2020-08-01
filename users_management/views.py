from django.shortcuts import render
from django.views.generic import View,DetailView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse
from users_management.models import UserProfile
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
   

        