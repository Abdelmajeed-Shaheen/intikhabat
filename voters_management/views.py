from django.shortcuts import render 
from django.views.generic import View
from django.http import JsonResponse


class CreateVoter(View):
    
    def post(self,request):
        return JsonResponse({"message":"success"})


class UpdateVoterProfile(View):

    def post(self,request):
        return JsonResponse({"message":"success"})

    