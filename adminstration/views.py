from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.generic import CreateView,View
from .models import Comittee
from users_management.models import ( 
                                        Candidate,CustomComitteePermission,
                                        CustomMembersPermissions,ComitteeMember
                                    )
from common.models import Address
from .forms import CreateComitteeForm
from users_management.forms import SignUpForm
import json



class CampaignManagementMainView(View):    
    model=Comittee

    def get(self,request):
        candidate=request.user.userprofile.candidate
        comittees_list=Comittee.objects.filter(is_active=True)
        campaign_manager=candidate.campaignadminstrator_set.first()
        comittees_members=candidate.comitteemember_set.all()

        context={
            "form":CreateComitteeForm,
            "comittee_member_form":SignUpForm,
            "comittees_list":comittees_list,
            "campaign_manager":campaign_manager,
            "comittees_members":comittees_members
        }
        return render(request,"adminstration.html",context)



class CreateComitteeView(View):

    def post(self,request):
        candidate=request.POST.get('candidate')
        candidate=Candidate.objects.get(pk=int(candidate))
        name=request.POST.get('name')
        description=request.POST.get('description')
        is_active=request.POST.get('is_active')
        if is_active == "on":
            is_active=True
        else:
            is_active=False
        address=request.POST.get('address')
        address=Address.objects.get(pk=int(address))
        response={
            'candidate':candidate,
            'name':name,
            'description':description,
            'is_active':is_active,
            'address':address
        }
        comittee=Comittee.objects.create(**response)
        print(comittee)

        return JsonResponse({"message":"success"})

class GrantPermissions(View):
    def post(self,request):
        user=request.POST.get('userId')
        if request.POST.get('userPerm'):
            user_perm=json.loads(request.POST.get('userPerm'))
            print(user_perm)

            comittee_member=ComitteeMember.objects.get(id=int(user))

            cmp_data={
                'user':comittee_member.profile,
                'can_view_member':user_perm['show'],
                'can_update_member':user_perm['edit'],
                'can_create_member':user_perm['create'],
                'can_remove_member':user_perm['delete']
            }
            custom_member_permission=CustomMembersPermissions(**cmp_data)
            custom_member_permission.save()
            print(custom_member_permission)
            
        if  request.POST.get('commPerm'):
            comm_perm=request.POST.get('commPerm')
            

        return JsonResponse({"message":"success"})
