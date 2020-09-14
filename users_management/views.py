from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import View,DetailView
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.db.utils import IntegrityError
from django.urls import reverse
from users_management.models import (UserProfile,ComitteeMember,
                                    CampaignAdminstrator,CommunicationOfficer,
                                    CustomVoterssPermissions,CustomMembersPermissions,
                                    CustomReportsPermissions,CustomComitteePermission,
                                     )
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
import re
from datetime import date
from .documents import VoterDocument
from elasticsearch_dsl import Q


def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

def hasLetters(inputString):

    return bool(re.search(r'[a-zA-Z]', inputString))


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
        login_to=request.POST.get('login_to')

        if UserProfile.objects.filter(mobile_number=username).exists():
            username=UserProfile.objects.get(mobile_number=username).user.username

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.is_active:

                if login_to=="camp":
                    if hasattr(user.userprofile, 'candidate') or hasattr(user.userprofile, 'campaignadminstrator'):

                        response['redirect_to']=reverse('main')

                    elif hasattr(user.userprofile,'comitteemember'):
                        response['redirect_to']=reverse('comittee-member')
                else:
                    if hasattr(user.userprofile, 'voter'):

                        response['redirect_to']=reverse('voter-profile',kwargs={'pk':user.userprofile.id})

                login(request, user)
                return JsonResponse(response)

            else:
                response["error"]="دخول غير مصرح به"

                return JsonResponse(response)
        else:

            response["error"]="اسم المستخدم او كلمة المرور غير صحيحة"

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
        exist=request.POST.get("exist")

        full_name=form.data.get('full_name')
        if hasNumbers(full_name):
            return JsonResponse({"error":"لا يمكن للاسماء ان تحتوي ارقام"})

        mobile_number=form.data.get('mobile_number')
        whatsapp_number=form.data.get('whatsapp_number')

        if hasLetters(mobile_number) or hasLetters(whatsapp_number):
            return JsonResponse({"error":"لا يمكن للارقام ان تحتوي احرف"})

        email=form.data.get('email')
        is_manager=form.data.get('is_manager')

        if is_manager == "on" :
            is_manager=True
        else:
            is_manager=False

        password='changeme12'
        user_type=request.POST.get('usertype')
        comittee=""
        if request.POST.get('comittee'):
            comittee=Comittee.objects.get(id=request.POST.get('comittee'))

        if not exist:

            try:

                user_instance={
                    'username':mobile_number,
                    'email':email
                }
                user=User(**user_instance)
                user.set_password(password)
                user.save()


                profile_instance={
                    'full_name':full_name,
                    'user':user,
                    'mobile_number':mobile_number,
                    'whatsapp_number':whatsapp_number,
                    'date_of_birth':date.today(),
                    'name_string':full_name.replace(" ","")

                }

                user_profile=UserProfile(**profile_instance)
                user_profile.save()

                vp={
                    'user':user_profile,
                    'can_view_voter':False,
                    'can_create_voter':False,
                    'can_update_voter':False,
                    'can_remove_voter':False
                }
                voter_permissions=CustomVoterssPermissions(**vp)

                rp={
                    'user':user_profile,
                    'can_view_report':False,
                    'can_create_report':False,
                    'can_update_report':False,
                    'can_remove_report':False
                }
                report_permissions=CustomReportsPermissions(**rp)

                cp={
                    'user':user_profile,
                    'can_view_comittee':False,
                    'can_create_comittee':False,
                    'can_update_comittee':False,
                    'can_remove_comittee':False
                }
                comittee_permissions=CustomComitteePermission(**cp)

                mp={
                    'user':user_profile,
                    'can_view_member':False,
                    'can_create_member':False,
                    'can_update_member':False,
                    'can_remove_member':False
                }
                member_permissions=CustomMembersPermissions(**mp)
                member_permissions.save()
                voter_permissions.save()
                report_permissions.save()
                comittee_permissions.save()

            except (IntegrityError):
                if User.objects.all().filter(username=user_instance["username"]).exists():
                    return JsonResponse({'error':'هذا المستخدم مسجل مسبقا'})

                elif UserProfile.objects.all().filter(name_string=name_string).exists():
                    return JsonResponse({'error':'هذا الاسم مكرر'})

        else:
            user_profile=UserProfile.objects.get(name_string=full_name.replace(" ",""))

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
            try:
                campaign_manager=CampaignAdminstrator(profile=user_profile,candidate=candidate)
                campaign_manager.save()
            except IntegrityError:
                camp_admin=CampaignAdminstrator.objects.get(candidate=candidate)
                camp_admin.profile=user_profile
                camp_admin.save()


        return JsonResponse({'message':'تم التسجيل بنجاح'})



class UpdateProfile(View):

    def post(self,request):
        userprofile=request.POST.get("user")
        userprofile=json.loads(userprofile)
        User.objects.filter(id=request.user.id).update(first_name=userprofile["first_name"],last_name=userprofile["last_name"])
        profile=UserProfile.objects.get(id=int(userprofile['id']))
        name_string=(userprofile['first_name']+userprofile['second_name']+userprofile['third_name']+userprofile['last_name'])
        if hasNumbers(name_string):
            return JsonResponse({"error":"الاسماء لا يمكن ان تحتوي على ارقام"})
        if hasLetters(userprofile["mobile_number"]) or hasLetters(userprofile["whatsapp_number"]):
            return JsonResponse({"error":"ارقام الهواتف لا يمكن ان تحتوي على احرف"})
        user_object={}
        empty=[None,""]

        if 'second_name' in userprofile and userprofile['second_name'] not in empty:
            user_object['middle_name']=userprofile['second_name']
            profile.middle_name=user_object['middle_name']

        if 'third_name' in userprofile and userprofile['third_name'] not in empty:
            user_object['last_name']=userprofile['third_name']
            profile.last_name=user_object['last_name']

        if 'mobile_number' in userprofile and userprofile['mobile_number'] not in empty:
            user_object['mobile_number']=userprofile['mobile_number']
            profile.mobile_number=user_object['mobile_number']

        if 'whatsapp_number' in userprofile and userprofile['whatsapp_number'] not in empty:
            user_object['whatsapp_number']=userprofile['whatsapp_number']
            profile.whatsapp_number=user_object['whatsapp_number']

        if 'district' in userprofile and userprofile['district'] not in empty:
            district=District.objects.get(id=int(userprofile['district']))
            address=profile.address
            address.district=district
            address.save()

        if 'title' in userprofile and userprofile['title'] is not None:
            if hasNumbers(userprofile['title']):
                return JsonResponse({"error":"لا يمكن للاسماء ان تحتوي ارقام"})
            else:
                candidate=request.user.userprofile.candidate
                candidate.title=userprofile['title']
                candidate.save()

        profile.save()
        return JsonResponse({"user":"success"})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'تم نغيير كلمة السر بنجاح')

            return redirect(reverse('password-change'))
        else:
            messages.error(request, 'يرجى مراعاة كلمة السر ان تتضمن ٨ خانات على الاقل و ارقام واحرف')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def check_user_elastic(request):
    if request.GET:
        name=request.GET.get("name")
        new_string='"'+name+'"'
        name_format='{0}'
        name_format=name_format.format(new_string)
        s = VoterDocument.search()
        s = s.query('query_string', query=name_format)
        response=[]

        for hit in s:
            hit=json.loads(hit.message)
            voter_object={}
            voter_object['name']=hit["elector_name"]
            voter_object['circle_name']=hit["circle_name"]
            voter_object['election_place_name']=hit["election_place_name"]
            voter_object['success']=True
            response.append(voter_object)
    else:
        voter_object={}
        voter_object['error']="لا يمكن تنفيذ طلبك حاليا"
        response.append(voter_object)

    return JsonResponse(response,safe=False)
