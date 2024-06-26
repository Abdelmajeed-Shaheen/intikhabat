from django.shortcuts import render
from users_management.forms import LoginForm,CandidateLoginForm
from users_management.models import WorkField
from voters_management.form import VoterRegForm
from common.models import (Governorate,
                           Department,
                            District,
                            Area,
                            Street
                           )

# Create your views here.
def home(request):
    login_form=LoginForm
    work_fields_list=WorkField.objects.all()
    voter_reg_form=VoterRegForm()
    candidate_login_form=CandidateLoginForm()
    governorates_list=Governorate.objects.all()
    context={
        'login_form':login_form,
        'voter_reg_form':voter_reg_form,
        'work_fields_list':work_fields_list,
        'candidate_login_form':candidate_login_form,
        'governorates_list':governorates_list
    }
    return render(request,'index.html',context)