from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.generic import CreateView,View
from .models import Comittee
from users_management.models import ( 
                                        Candidate,CustomComitteePermission,
                                        CustomMembersPermissions,ComitteeMember
                                    )
from common.models import ( Address,
                            Department,
                            Governorate,
                            District, 
                            Area)

from .forms import CreateComitteeForm
from users_management.forms import SignUpForm
import json



class CampaignManagementMainView(View):    
    model=Comittee

    def get(self,request):
        if hasattr(request.user.userprofile,'campaignadminstrator'):
            candidate=request.user.userprofile.campaignadminstrator.candidate
        else:
            candidate=request.user.userprofile.candidate
        user=request.user.userprofile
        comittees_list=Comittee.objects.filter(is_active=True)
        campaign_manager=candidate.campaignadminstrator_set.first()
        comittees_members=candidate.comitteemember_set.all()
        govenorate_list=Governorate.objects.all()
        departments_list=Department.objects.all()
        areas_list=Area.objects.all()
        districts_list=District.objects.all()
            

        context={
            "form":CreateComitteeForm,
            "comittee_member_form":SignUpForm,
            "comittees_list":comittees_list,
            "campaign_manager":campaign_manager,
            "comittees_members":comittees_members,
            "user":user,
            "govenorate_list":govenorate_list,
            "candidate":candidate,
            "departments_list":departments_list,
            "areas_list":areas_list,
            "districts_list":districts_list
        }
        return render(request,"adminstration.html",context)

class ComitteeMemberView(View):    

    def get(self,request):
        
        comittee=request.user.userprofile.comitteemember.comittee
        candidate=request.user.userprofile.comitteemember.candidate
        user=request.user.userprofile
        campaign_manager=candidate.campaignadminstrator_set.first()
        comittees_members=comittee.comitteemember_set.all()
        addresses_list=Address.objects.all()
            
        context={
            "comittee_member_form":SignUpForm,
            "campaign_manager":campaign_manager,
            "comittees_members":comittees_members,
            "user":user,
            "comittee":comittee,
            "addresses_list":addresses_list
        }
        return render(request,"adminstration_cm.html",context)

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
        comittee_member=ComitteeMember.objects.get(id=int(user))
        if request.POST.get('userPerm'):
            user_perm=json.loads(request.POST.get('userPerm'))
            

            cmp_data={
                'user':comittee_member.profile,
                'can_view_member':user_perm['show'],
                'can_update_member':user_perm['edit'],
                'can_create_member':user_perm['create'],
                'can_remove_member':user_perm['delete']
            }
            custom_member_permission=CustomMembersPermissions(**cmp_data)
            custom_member_permission.save()
            
            
        if  request.POST.get('commPerm'):
            comm_perm=json.loads(request.POST.get('commPerm'))
            ccp_data={
                'user':comittee_member.profile,
                'can_view_comittee':comm_perm['show'],
                'can_update_comittee':comm_perm['edit'],
                'can_create_comittee':comm_perm['create'],
                'can_remove_comittee':comm_perm['delete']               
            }
            comittee_permissions=CustomComitteePermission(**ccp_data)
            comittee_permissions.save()

        return JsonResponse({"message":"success"})


class SearchComitteeView(View):

    def get(self,request):
        query=request.GET.get('query')
        print(query)

        return JsonResponse({"message":"success"})

class CreateAreaView(View):

    def post(self,request):
        address=request.user.userprofile.address
        area_object={}
        area_name=request.POST.get("area_name")
        dept_id=int(request.POST.get("dept"))
        dept=Department.objects.get(id=dept_id)
        area_object['name']=area_name
        area_object['department']=dept
        area=Area(**area_object)
        area.save()
        address.area=area
        address.save()

        return JsonResponse({"message":"success"})

class CreateDistrictView(View):

    def post(self,request):
        address=request.user.userprofile.address
        dist_object={}
        dist_name=request.POST.get("dist_name")
        area_id=int(request.POST.get("area"))
        area=Area.objects.get(id=area_id)
        dist_object['name']=dist_name
        dist_object['area']=area
        dist=District(**dist_object)
        dist.save()
        address.district=dist
        address.save()

        return JsonResponse({"message":"success"})
        