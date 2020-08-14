from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.generic import CreateView,View,ListView
from django.db.models import Q
from .models import Comittee
from users_management.models import ( 
                                        Candidate,CustomComitteePermission,
                                        CustomMembersPermissions,ComitteeMember,
                                        Voter
                                    )
from common.models import ( Address,
                            Department,
                            Governorate,
                            District, 
                            Area)

from .forms import CreateComitteeForm
from users_management.forms import SignUpForm
import json
# testing purpose
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML,CSS

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
    paragraphs = ['يحى', 'صلاح', 'البشار']
    html_string = render_to_string('report.html', {'paragraphs': paragraphs})
    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    css=CSS('/home/yahya/Dev/dev_jpems/intikhabat/common/static/common/vendor/bootstrap/css/bootstrap.css')
    html.write_pdf(target='/tmp/mypdf.pdf',stylesheets=[css])

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
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

        
        comittee_members_list=ComitteeMember.objects.filter(candidate=candidate)
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
        print(query)

        return JsonResponse({"message":"success"})


class GetVotersList(View):

    def get(self,request):
        
        response=[]
        query=request.GET.get('query')
        print(query)
        query=json.loads(query)
        search_object={}
        data={}
        if 'cm_id' in query and query['cm_id'] not in [None,""]:
            cm=ComitteeMember.objects.get(id=int(query['cm_id']))
            search_object['profile__address__district']=cm.profile.address.district
            search_object['candidate']=cm.candidate

        if 'is_identifier' in query and query['is_identifier'] not in [None,""]:
                identifier_object={
                    'is_identifier':True
                }
                if query['identifier_name'] not in [None,""]:

                    identifier_name=query['identifier_name']
                    identifier_name=identifier_name.replace(" ","")
                    identifier_object["profile__name_string"]=identifier_name
                
                if  query['identifier_wa'] not in [None,""]:
                    identifier_object['profile__whatsapp_number']=query['identifier_wa']

                identifier=Voter.objects.get(**identifier_object,candidate=cm.candidate)
                search_object["identiefier"]=identifier
                
                if  query['identifier_mobile'] not in [None,""]:
                    identifier_object['profile__mobile_number']=query['identifier_mobile']

                identifier_response={}
                identifier_response['idn_name']=(identifier.profile.user.first_name+" "+identifier.profile.middle_name+" "+identifier.profile.last_name+" "+identifier.profile.user.last_name)
                data["identifier"]=identifier_response 
                

        if query['area_id'] not in [None,""]:
            area=Area.objects.get(id=int(query['area_id']))
            search_object['profile__address__area']=area

        if query['gover_id'] not in [None,""]:
            governorate=Governorate.objects.get(id=int(query['gover_id']))
            search_object['profile__address__governorate']=governorate

        if query['dept_id'] not in [None,""]:
            dept=Department.objects.get(id=int(query['dept_id']))
            search_object['profile__address__department']=dept
        print(search_object)
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
    search_object={}
    if query['cm_id'] not in [None,""]:
        cm=ComitteeMember.objects.get(id=int(query['cm_id']))
        search_object['profile__address__district']=cm.profile.address.district
        search_object['candidate']=cm.candidate
        
    if query['area_id'] not in [None,""]:
        area=Area.objects.get(id=int(query['area_id']))
        search_object['profile__address__area']=area

    if query['gover_id'] not in [None,""]:
        governorate=Governorate.objects.get(id=int(query['gover_id']))
        search_object['profile__address__governorate']=governorate

    if query['dept_id'] not in [None,""]:
        dept=Department.objects.get(id=int(query['dept_id']))
        search_object['profile__address__department']=dept
    
    voters_list=Voter.objects.filter(**search_object)
    
    html_string = render_to_string('by_cm_report.html', {'voters_list': voters_list})
    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    css=CSS('/home/yahya/Dev/dev_jpems/intikhabat/common/static/common/vendor/bootstrap/css/bootstrap.css')
    html.write_pdf(target='/tmp/mypdf.pdf',stylesheets=[css])
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


def by_identifier_report(request):

    query=request.GET.get('query')
    query=json.loads(query)
    search_object={}
    display_idn_name=""
    if query['cm_id'] not in [None,""]:
        cm=ComitteeMember.objects.get(id=int(query['cm_id']))
        search_object['profile__address__district']=cm.profile.address.district
        search_object['candidate']=cm.candidate

    if query['is_identifier']:
            identifier_object={
                'is_identifier':True
            }
            if query['identifier_name'] not in [None,""]:
                
                identifier_name=query['identifier_name']
                name=identifier_name.replace(" ","")
                identifier_object["profile__name_string"]=name
            
            if  query['identifier_wa'] not in [None,""]:
                identifier_object['profile__whatsapp_number']=query['identifier_wa']

            identifier=Voter.objects.get(**identifier_object,candidate=cm.candidate)
            display_idn_name=identifier
            search_object["identiefier"]=identifier
            
            if  query['identifier_mobile'] not in [None,""]:
                identifier_object['profile__mobile_number']=query['identifier_mobile']            


    if query['area_id'] not in [None,""]:
        area=Area.objects.get(id=int(query['area_id']))
        search_object['profile__address__area']=area

    if query['gover_id'] not in [None,""]:
        governorate=Governorate.objects.get(id=int(query['gover_id']))
        search_object['profile__address__governorate']=governorate

    if query['dept_id'] not in [None,""]:
        dept=Department.objects.get(id=int(query['dept_id']))
        search_object['profile__address__department']=dept
    voters_list=Voter.objects.filter(**search_object)
    
    html_string = render_to_string('by_idn_report.html', {'voters_list': voters_list,'display_idn_name':display_idn_name})
    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    css=CSS('/home/yahya/Dev/dev_jpems/intikhabat/common/static/common/vendor/bootstrap/css/bootstrap.css')
    html.write_pdf(target='/tmp/by_identifier_report.pdf',stylesheets=[css])
    fs = FileSystemStorage('/tmp')
    with fs.open('by_identifier_report.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="by_identifier_report.pdf"'
    return response


class GetVotersByAddressReport(View):
    template_name="address_report.html"
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



def by_address_report(request):

    query=request.GET.get('query')
    query=json.loads(query)
    search_object={}

    if 'cm_id' in query and query['cm_id'] not in [None,""]:
        cm=ComitteeMember.objects.get(id=int(query['cm_id']))
        search_object['profile__address__district']=cm.profile.address.district
        search_object['candidate']=cm.candidate
    else:
        if hasattr(request.user.userprofile,'candidate') or hasattr(request.user.userprofile,'campaignadminstrator'):
            search_object['candidate']=request.user.userprofile.candidate
        
        else:
            search_object['candidate']=request.user.userprofile.comitteemanager.candidate
        

        
    if query['area_id'] not in [None,""]:
        area=Area.objects.get(id=int(query['area_id']))
        search_object['profile__address__area']=area

    if query['gover_id'] not in [None,""]:
        governorate=Governorate.objects.get(id=int(query['gover_id']))
        search_object['profile__address__governorate']=governorate

    if query['dept_id'] not in [None,""]:
        dept=Department.objects.get(id=int(query['dept_id']))
        search_object['profile__address__department']=dept
    
    voters_list=Voter.objects.filter(**search_object)
    
    html_string = render_to_string('by_cm_report.html', {'voters_list': voters_list})
    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    css=CSS('/home/yahya/Dev/dev_jpems/intikhabat/common/static/common/vendor/bootstrap/css/bootstrap.css')
    html.write_pdf(target='/tmp/mypdf.pdf',stylesheets=[css])
    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    return response

def by_status_report(request):

    query=request.GET.get('query')
    query=json.loads(query)
    search_object={}
    if query['cm_id'] not in [None,""]:
        cm=ComitteeMember.objects.get(id=int(query['cm_id']))
        search_object['profile__address__district']=cm.profile.address.district
        search_object['candidate']=cm.candidate
        
    if query['area_id'] not in [None,""]:
        area=Area.objects.get(id=int(query['area_id']))
        search_object['profile__address__area']=area

    if query['gover_id'] not in [None,""]:
        governorate=Governorate.objects.get(id=int(query['gover_id']))
        search_object['profile__address__governorate']=governorate

    if query['dept_id'] not in [None,""]:
        dept=Department.objects.get(id=int(query['dept_id']))
        search_object['profile__address__department']=dept
    
    voters_list=Voter.objects.filter(**search_object)
    
    html_string = render_to_string('by_status_report.html', {'voters_list': voters_list})
    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    css=CSS('/home/yahya/Dev/dev_jpems/intikhabat/common/static/common/vendor/bootstrap/css/bootstrap.css')
    html.write_pdf(target='/tmp/by_status_report.pdf',stylesheets=[css])
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