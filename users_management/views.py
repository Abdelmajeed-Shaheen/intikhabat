from django.shortcuts import render
from django.views.generic import View
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
        print(username)
        if UserProfile.objects.filter(mobile_number=username).exists():
            username=UserProfile.objects.get(mobile_number=username).user.username

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                if hasattr(user.userprofile, 'candidate'):
                    print("success")
                    # login(request, user)

                    return HttpResponse("hello user")

            else:
                messages.error(request,'Your profile is not activated yet.')
        else:
            print("fail")
            response["error"]="invalid username or password"
            return JsonResponse(response)
    
                

        