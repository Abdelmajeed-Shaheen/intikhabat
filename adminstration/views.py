from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.views.generic import CreateView,View,ListView
from django.db.models import Q
from .models import Comittee
from users_management.models import ( 
                                        Candidate,
                                        ComitteeMember,Voter,
                                        CustomVoterssPermissions,CustomMembersPermissions,
                                        CustomReportsPermissions,CustomComitteePermission,
                                        CampaignAdminstrator
                                    )
from common.models import ( Address,
                            Department,
                            Governorate,
                            District, 
                            Area)

from .forms import CreateComitteeForm,UpdateCmForm
from users_management.forms import SignUpForm
import json
# testing purpose
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from weasyprint import HTML

import json


class CampaignManagementMainView(View):    
    model=Comittee

    def get(self,request):
        if hasattr(request.user.userprofile,'campaignadminstrator'):
            candidate=request.user.userprofile.campaignadminstrator.candidate
        else:
            candidate=request.user.userprofile.candidate
        user=request.user.userprofile
        comittees_list=Comittee.objects.filter(is_active=True,candidate=candidate)
        campaign_manager=candidate.campaignadminstrator
        comittees_members=candidate.comitteemember_set.all()
        govenorate_list=Governorate.objects.all()
        departments_list=Department.objects.all()
        areas_list=Area.objects.all()
        districts_list=District.objects.all()
        new_voters_list=Voter.objects.all().filter(followed_up=False,candidate=candidate).order_by("-id")
            
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
            "districts_list":districts_list,
            "new_voters_list":new_voters_list
        }
        return render(request,"adminstration.html",context)

class ComitteeMemberView(View):    

    def get(self,request):
        
        comittee=request.user.userprofile.comitteemember.comittee
        candidate=request.user.userprofile.comitteemember.candidate
        user=request.user.userprofile
        campaign_manager=candidate.campaignadminstrator
        comittees_members=comittee.comitteemember_set.all()
        voters_permissions=CustomVoterssPermissions.objects.get(user=user)
        reports_permissions=CustomReportsPermissions.objects.get(user=user)
        comittees_permissions=CustomComitteePermission.objects.get(user=user)
        memebrs_permissions=CustomMembersPermissions.objects.get(user=user)
        
        if user.comitteemember.is_manager:
            new_voters_list=Voter.objects.all().filter(candidate=candidate,followed_up=False)
        else:
            new_voters_list=Voter.objects.all().filter(related_comittee_member=user.comitteemember,followed_up=False)
        
            
        context={
            "comittee_member_form":SignUpForm,
            "campaign_manager":campaign_manager,
            "comittees_members":comittees_members,
            "user":user,
            "comittee":comittee,
            "new_voters_list":new_voters_list,
            "voters_permissions":voters_permissions,
            "reports_permissions":reports_permissions,
            "members_permissions":memebrs_permissions,
            "comittees_permissions":comittees_permissions
        }
        return render(request,"adminstration_cm.html",context)

class CreateComitteeView(View):

    def post(self,request):
        
        if hasattr(request.user.userprofile,'candidate'):
            candidate=Candidate.objects.get(pk=request.user.userprofile.candidate.id)
        elif hasattr(request.user.userprofile,'campaignadminstrator'):
            candidate=request.user.userprofile.campaignadminstrator.candidate    
        name=request.POST.get('name')
        description=request.POST.get('description')
        is_active=request.POST.get('status')
        print(is_active)
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
        profile=comittee_member.profile

        if request.POST.get('memberPerm'):
            member_perm=json.loads(request.POST.get('memberPerm'))
            cmp_data={
                'user':profile,
                'can_view_members':member_perm['show'],
                'can_update_member':member_perm['edit'],
                'can_create_member':member_perm['create'],
                'can_remove_member':member_perm['delete']               
            }
            member_permissions=CustomMembersPermissions.objects.get(user=profile)
            member_permissions.can_view_member=cmp_data['can_view_members']
            member_permissions.can_update_member=cmp_data['can_update_member']
            member_permissions.can_create_member=cmp_data['can_create_member']
            member_permissions.can_remove_member=cmp_data['can_remove_member']
            member_permissions.save()

        if request.POST.get('voterPerm'):
            voter_perms=json.loads(request.POST.get('voterPerm'))
            cvp_data={
                'user':profile,
                'can_view_voter':voter_perms['show'],
                'can_update_voter':voter_perms['edit'],
                'can_create_voter':voter_perms['create'],
                'can_remove_voter':voter_perms['delete']               
            }
            # print(cvp_data)
            voter_permissions=CustomVoterssPermissions.objects.get(user=profile)
            voter_permissions.can_view_voter=cvp_data['can_view_voter']
            voter_permissions.can_update_voter=cvp_data['can_update_voter']
            voter_permissions.can_create_voter=cvp_data['can_create_voter']
            voter_permissions.can_remove_voter=cvp_data['can_remove_voter']
 
            voter_permissions.save()

        if request.POST.get('reportPerm'):
            report_perms=json.loads(request.POST.get('reportPerm'))
            crp_data={
                'user':profile,
                'can_view_report':report_perms['show'],
                'can_update_report':report_perms['edit'],
                'can_create_report':report_perms['create'],
                'can_remove_report':report_perms['delete']               
            }
            # print(cvp_data)
            report_permissions=CustomReportsPermissions.objects.get(user=profile)
            report_permissions.can_view_report=crp_data['can_view_report']
            report_permissions.can_update_report=crp_data['can_update_report']
            report_permissions.can_create_report=crp_data['can_create_report']
            report_permissions.can_remove_report=crp_data['can_remove_report']
 
            report_permissions.save()


        if request.POST.get('commPerm'):
            comm_perm=json.loads(request.POST.get('commPerm'))
            ccp_data={
                'user':profile,
                'can_view_comittee':comm_perm['show'],
                'can_update_comittee':comm_perm['edit'],
                'can_create_comittee':comm_perm['create'],
                'can_remove_comittee':comm_perm['delete']               
            }
            comittee_permissions=CustomComitteePermission.objects.get(user=profile)
            comittee_permissions.can_view_comittee=ccp_data['can_view_comittee']
            comittee_permissions.can_update_comittee=ccp_data['can_update_comittee']
            comittee_permissions.can_create_comittee=ccp_data['can_create_comittee']
            comittee_permissions.can_remove_comittee=ccp_data['can_remove_comittee']
            comittee_permissions.save()
            # print("ccp to: ",comittee_permissions.user)

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

def html_to_pdf_view(request):
    if hasattr(request.user.userprofile,'comitteemanager'):
        cm=ComitteeMember.objects.get(id=request.user.userprofile.comitteemember.id)
        if cm.is_manager:
            voters_list=Voter.objects.all().filter(candidate=cm.candidate,has_elc_card=True)
        else:
            voters_list=Voter.objects.all().filter(related_comittee_member=cm,has_elc_card=True)


    elif hasattr(request.user.userprofile,'campaignadminstrator'):
        ca=CampaignAdminstrator.objects.get(id=request.user.userprofile.campaignadminstrator.id)
        voters_list=Voter.objects.all().filter(candidate=ca.candidate,has_elc_card=True)

    elif hasattr(request.user.userprofile,'candidate'):
        candi=Candidate.objects.get(id=request.user.userprofile.candidate.id)
        voters_list=Voter.objects.all().filter(candidate=candi,has_elc_card=True)

    html_string = render_to_string('report.html', {'voters_list': voters_list})
    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/election_cards.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('election_cards.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="election_cards.pdf"'
    return response



class GetReportByCommitteeMember(ListView):
    template_name="cm_report.html"
    def get(self,request):
        governorates_list=Governorate.objects.all()

        if hasattr(request.user.userprofile,'campaignadminstrator'):
            candidate=request.user.userprofile.campaignadminstrator.candidate
        
        elif hasattr(request.user.userprofile,'comitteemember'):
            candidate=request.user.userprofile.comitteemember.candidate

        else :
            candidate=request.user.userprofile.candidate

        
        comittee_members_list=candidate.comitteemember_set.all()
        context={
            'gover_list':governorates_list,
            'cm_members_list':comittee_members_list
            
        }
        
        return render(request,self.template_name,context)


class GetGovernorateDepartment(View):

    def get(self,request):
        response=[]
        gover_id=request.GET.get('gover_id')
        governorate=Governorate.objects.get(id=int(gover_id))
        dept_list=Department.objects.filter(governorate=governorate)

        for dept in dept_list:
            item={}
            item['name']=dept.name
            item['id']=dept.id
            response.append(item)
        
        return JsonResponse(response,safe=False)

class GetDepartmentArea(View):

    def get(self,request):
        response=[]
        dept_id=request.GET.get('dept_id')
        dept=Department.objects.get(id=int(dept_id))
        areas_list=Area.objects.filter(department=dept)

        for area in areas_list:
            item={}
            item['name']=area.name
            item['id']=area.id
            response.append(item)
        
        return JsonResponse(response,safe=False)

class SearchComitteeView(View):

    def get(self,request): 
        query=request.GET.get('query')
        
        response=[]
        try:
            comittee=Comittee.objects.get(name=query)         
            if comittee.is_active:
                status="فعالة"
            else:
                status="غير فعالة"
            
            if comittee.manager is not None:
                manager=str(comittee.manager.profile.user.first_name+" " +comittee.manager.profile.user.last_name)
            else:
                manager="لا يوجد مدير"
            comittee={
                'comittee_name':comittee.name,
                'status':status,
                'manager':manager,
                'id':comittee.id
            }
            response.append(comittee)
            return JsonResponse({"comittee":comittee})
        except:
            response.append('لا توجد نتائج')
            return JsonResponse({"error":response})


class GetVotersList(View):

    def get(self,request):
        
        response=[]
        query=request.GET.get('query')
        query=json.loads(query)
        search_object={}
        data={}
        identifier_object={}

        if 'status' in query:
            search_object['vote_status']=query['status']
        else:
            search_object['vote_status']="Voting"

        if 'is_identifier' in query and query['is_identifier'] not in [None,""]:                    
                identifier_object['is_identifier']=True

        if 'cm_id' in query and query['cm_id'] not in [None,""]:
            cm=ComitteeMember.objects.get(id=int(query['cm_id']))
            identifier_object["related_comittee_member"]=cm
            search_object['related_comittee_member']=cm

        if 'identifier' in query and query['identifier_id'] not in [None,""]:

            identifier_id=query['identifier_id']
            identifier_object["id"]=identifier_id
        
        if 'identifier_wa' in query and query['identifier_wa'] not in [None,""]:
            identifier_object['profile__whatsapp_number']=query['identifier_wa']


        
        if 'identifier_mobile' in query and query['identifier_mobile'] not in [None,""]:
            identifier_object['profile__mobile_number']=query['identifier_mobile']
        try:
            identifier=Voter.objects.get(**identifier_object)
            search_object["identiefier"]=identifier
            identifier_response={}
            identifier_response['idn_name']=(identifier.profile.user.first_name+" "+identifier.profile.middle_name+" "+identifier.profile.last_name+" "+identifier.profile.user.last_name)
            data["identifier"]=identifier_response
        except:
            pass

 
        if 'area_id' in query and query['area_id'] not in [None,""]:
            area=Area.objects.get(id=int(query['area_id']))
            search_object['profile__address__area']=area

            if 'district' in query:
                search_object["profile__address__district"]=query['district']
            
            candidate=Candidate.objects.get(id=int(query['candidate']))

            search_object['candidate']=candidate
        
        if query['gender'] not in [None,""]:
            search_object['profile__gender']=query['gender']
        
        voters_list=Voter.objects.filter(**search_object)
  
       
        for voter in voters_list:
            obj={}
            obj['id']=voter.id
            obj['full_name']=(voter.profile.user.first_name+" "+voter.profile.user.last_name)
            obj['mobile_no']=voter.profile.mobile_number
            if voter.identiefier:
                obj['identifier']=(voter.identiefier.profile.user.first_name+" "+voter.identiefier.profile.user.last_name)
                obj['identifier_phone_no']=voter.identiefier.profile.mobile_number
                obj['identifier_whats_no']=voter.identiefier.profile.whatsapp_number
            else:
                obj['identifier']='لا يوجد'
                obj['identifier_phone_no']='لا يوجد'
                obj['identifier_whats_no']='لا يوجد'

            if voter.has_elc_card:
                obj['has_elc_card']='نعم'
            else:
                obj['has_elc_card']='لا'
           
                
            response.append(obj)

 
        data['data']=response
        return JsonResponse(data,safe=False)


def by_committee_member_report(request):

    query=request.GET.get('query')
    query=json.loads(query)
    search_object={'vote_status':"Voting"}
    if query['gender'] not in [None,""]:
        search_object['profile__gender']=query['gender']
    if query['cm_id'] not in [None,""]:
        cm=ComitteeMember.objects.get(id=int(query['cm_id']))
        search_object['related_comittee_member']=cm
    voters_list=Voter.objects.filter(**search_object)
    html_string = render_to_string('by_cm_report.html', {'voters_list': voters_list})
    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/mypdf.pdf',)
    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    return response



class GetReportByIdentifier(View):
    template_name="identifier_report.html"
    def get(self,request):
        governorates_list=Governorate.objects.all()

        if hasattr(request.user.userprofile,'campaignadminstrator'):
            candidate=request.user.userprofile.campaignadminstrator.candidate
        
        if hasattr(request.user.userprofile,'comitteemember'):
            candidate=request.user.userprofile.comitteemember.candidate

        else :
            candidate=request.user.userprofile.candidate
        comittee_members_list=ComitteeMember.objects.filter(candidate=candidate)


        context={
            'gover_list':governorates_list,
            'cm_members_list':comittee_members_list
            
        }
        
        return render(request,self.template_name,context)


def by_identifier_report(request):

    query=request.GET.get('query')
    query=json.loads(query)
    search_object={}
    identifier_object={}
    display_idn_name=""
    if query['cm_id'] not in [None,""]:
        cm=ComitteeMember.objects.get(id=int(query['cm_id']))
        identifier_object['related_comittee_member']=cm
        search_object['related_comittee_member']=cm
    if query["gender"] not in [None,""]:
        search_object["profile__gender"]=query["gender"]
    if query['is_identifier']:
            identifier_object['is_identifier']=True
        
            if query['identifier_id'] not in [None,""]:
                identifier_id=query['identifier_id']
                identifier_object["id"]=identifier_id
            
            if  query['identifier_wa'] not in [None,""]:
                identifier_object['profile__whatsapp_number']=query['identifier_wa']

            identifier=Voter.objects.get(**identifier_object)
            display_idn_name=identifier
            search_object["identiefier"]=identifier
            
            if  query['identifier_mobile'] not in [None,""]:
                identifier_object['profile__mobile_number']=query['identifier_mobile']
    voters_list=Voter.objects.filter(**search_object,vote_status="Voting")
    
    html_string = render_to_string('by_idn_report.html', {'voters_list': voters_list,'display_idn_name':display_idn_name})
    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/by_identifier_report.pdf')
    fs = FileSystemStorage('/tmp')
    with fs.open('by_identifier_report.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="by_identifier_report.pdf"'
    return response


class GetVotersByAddressReport(View):
    template_name="address_report.html"
    def get(self,request):
        user=request.user.userprofile
        reports_permissions=None
        if hasattr(request.user.userprofile,'campaignadminstrator'):
            candidate=request.user.userprofile.campaignadminstrator.candidate
        
        elif hasattr(request.user.userprofile,'comitteemember'):
            reports_permissions=CustomReportsPermissions.objects.get(user=user)
            candidate=request.user.userprofile.comitteemember.candidate

        else :
            candidate=request.user.userprofile.candidate

        areas_list=Area.objects.filter(department=candidate.election_list.election_address.department)        
        context={
            'areas_list':areas_list,
            'candidate':candidate,
            'reports_permissions':reports_permissions            
        }
        
        return render(request,self.template_name,context)



def by_address_report(request):

    query=request.GET.get('query')
    query=json.loads(query)
    search_object={}
    if query["gender"] not in [None,""]:
        search_object["profile__gender"]=query["gender"]
    if query['area_id'] not in [None,""]:
        search_object['profile__address__area']=Area.objects.get(id=int(query['area_id']))

        if query['district'] not in [None,""]:
            search_object['profile__address__district']=District.objects.get(id=int(query['district']))
        candidate=Candidate.objects.get(id=int(query['candidate']))
        search_object['candidate']=candidate
    
    voters_list=Voter.objects.filter(**search_object)
    
    html_string = render_to_string('by_cm_report.html', {'voters_list': voters_list})
    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/mypdf.pdf')
    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    return response

def by_status_report(request):

    query=request.GET.get('query')
    query=json.loads(query)
    search_object={}
    if query["gender"] not in [None,""]:
        search_object["profile__gender"]=query["gender"]
    if query['cm_id'] not in [None,""]:
        cm=ComitteeMember.objects.get(id=int(query['cm_id']))
        search_object['profile__address__district']=cm.profile.address.district
        search_object['candidate']=cm.candidate
    try:
        voters_list=Voter.objects.filter(candidate=cm.candidate,vote_status="Not_sure")
    except:
        if hasattr(request.user.userprofile,"candidate"):
            candidate=request.user.userprofile.candidate
            voters_list=Voter.objects.filter(candidate=candidate,vote_status="Not_sure")

        elif hasattr(request.user.userprofile,"campaignadminstrator"):
            candidate=request.user.userprofile.campaignadminstrator.candidate
            voters_list=Voter.objects.filter(candidate=candidate,vote_status="Not_sure")

    
    html_string = render_to_string('by_status_report.html', {'voters_list': voters_list})
    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/by_status_report.pdf')
    fs = FileSystemStorage('/tmp')
    with fs.open('by_status_report.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="by_status_report.pdf"'
    return response



class GetVotersByStatusReport(View):
    template_name="status_report.html"
    def get(self,request):
        governorates_list=Governorate.objects.all()

        if hasattr(request.user.userprofile,'campaignadminstrator'):
            candidate=request.user.userprofile.campaignadminstrator.candidate
        
        elif hasattr(request.user.userprofile,'comitteemember'):
            candidate=request.user.userprofile.comitteemember.candidate

        else :
            candidate=request.user.userprofile.candidate

        
        comittee_members_list=ComitteeMember.objects.filter(candidate=candidate)
        context={
            'gover_list':governorates_list,
            'cm_members_list':comittee_members_list
            
        }
        
        return render(request,self.template_name,context)



def update_comittee(request,id):
    comittee=Comittee.objects.get(id=id)
    update_form=CreateComitteeForm(instance=comittee)
    print(request.POST)
    if request.POST:
        name=request.POST.get('name')
        description=request.POST.get('description')
        if request.POST.get('is_active') == "on":
            is_active=True
        else:
            is_active=False
        address=Address.objects.get(id=int(request.POST.get('address')))

        comittee.name=name
        comittee.is_active=is_active
        comittee.description=description
        comittee.address=address
        comittee.save()

        return HttpResponseRedirect(reverse('update-committee',kwargs={'id':comittee.id}))

    context={
        'comittee':comittee,
        'update_form':update_form
    }
    return render(request,"update_comittee.html",context)



def update_comittee_member(request,id):
    cm=ComitteeMember.objects.get(id=id)
    candidate=cm.candidate
    comittees_list=candidate.comittee_candidate.all()
    department=candidate.election_list.election_address.department
    areas_list=Area.objects.filter(department=department)
    
    if request.POST:
        print(request.POST)
        comittee=request.POST.get('comittee')

        if request.POST.get('is_manager') == "on":
            is_manager=True
        else:
            is_manager=False

        profile=cm.profile
        if request.POST.get('is_active') =='on':
            is_active=True
        else:
            is_active=False
        cm.is_active=is_active
      
        if not cm.profile.address:
            governorate=candidate.election_list.election_address.governorate
            address=Address(governorate=governorate,department=department)
            address.save()
            
            profile.address=address
            profile.save()

        else:
            address=cm.profile.address
        
        if request.POST.get('area'):
            area=request.POST.get('area')
            address.area=Area.objects.get(id=int(area))
        
        if request.POST.get('district'):
            district=request.POST.get('district')
            address.district=District.objects.get(id=int(district))
        
        address.save()
        
        
        comittee=Comittee.objects.get(id=int(comittee))
        cm.comittee=comittee
        cm.is_manager=is_manager
        comittee.manager=cm
        comittee.save()
        cm.save()
        address.save()

    context={
        'cm':cm,
        'comittees_list':comittees_list,
        "areas_list":areas_list
        
    }
    return render(request,"update_cm.html",context)



def get_cm(request):
    term=request.GET.get("term")
    qs = ComitteeMember.objects.filter(Q(profile__user__first_name__icontains=term)|
                                      Q(profile__user__last_name__icontains=term)|
                                      Q(profile__middle_name__icontains=term)|
                                      Q(profile__last_name__icontains=term)
    )
    
    cm_list = []
    for cm in qs:
        cm={
            'lable':str(cm.profile.user.first_name+" "+cm.profile.user.last_name),
            'id':cm.id
        }
        cm_list.append(cm)
    
    return JsonResponse(cm_list, safe=False)
def get_cm_by_comittee(request):
    cm_id=request.GET.get("cm_id")
    comittee=Comittee.objects.get(id=int(request.GET.get("comittee")))
    qs = ComitteeMember.objects.filter(Q(id=int(cm_id))|
                                      Q(comittee=comittee)
                                       )
    
    cm_list = []
    for cm in qs:
        
            
        cm_obj={
            'name':str(cm.profile.user.first_name+" "+cm.profile.user.last_name),
            'phone_number':cm.profile.mobile_number,
            'email':cm.profile.user.email,
            'comittee':comittee.name,
            'id':cm.id,
        
        }
        if cm.is_manager:
            cm_obj['status']="مدير"
        else:
            cm_obj['status']="عضو"
            
        cm_list.append(cm_obj)
    
    return JsonResponse(cm_list, safe=False)
def get_identifier(request):
    term=request.GET.get("term")
    qs = Voter.objects.filter(Q(profile__user__first_name__icontains=term)|
                                      Q(profile__user__last_name__icontains=term)|
                                      Q(profile__middle_name__icontains=term)|
                                      Q(profile__last_name__icontains=term),
                                      is_identifier=True
    )
    
    cm_list = []
    for cm in qs:
        cm={
            'lable':str(cm.profile.user.first_name+" "+cm.profile.user.last_name),
            'id':cm.id
        }
        cm_list.append(cm)
    
    return JsonResponse(cm_list, safe=False)


def update_voter(request,id):
    voter=Voter.objects.get(id=id)
    if hasattr(request.user.userprofile,"campaignadminstrator") or hasattr(request.user.userprofile,"candidate"):
        cm_list=ComitteeMember.objects.filter(candidate=voter.candidate)
    
    elif request.user.userprofile.comitteemember.is_manager :
        cm_list=ComitteeMember.objects.filter(comittee=request.user.userprofile.comitteemember.comittee)

    if request.POST:
        cm=request.POST.get('cm')
        followed_up=request.POST.get('is_followed')
        if followed_up == 'on':
            followed_up=True
        else:
            followed_up=False
            
        cm=ComitteeMember.objects.get(id=int(cm))
        voter.related_comittee_member=cm
        voter.followed_up=followed_up
    voter.save()

    context={
        'voter':voter,
        'cm_list':cm_list
        
    }
    return render(request,"edit_voter.html",context)



class GetDistrict(View):

    def get(self,request):
        response=[]
        area_id=request.GET.get('area_id')
        area=Area.objects.get(id=int(area_id))
        districts_list=District.objects.filter(area=area)

        for district in districts_list:
            item={}
            item['name']=district.name
            item['id']=district.id
            response.append(item)
        
        return JsonResponse(response,safe=False)
