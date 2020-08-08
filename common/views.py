from django.shortcuts import render
from users_management.forms import LoginForm
from users_management.models import WorkField
from voters_management.form import VoterRegForm

# Create your views here.
def home(request):
    login_form=LoginForm
    work_fields_list=WorkField.objects.all()
    voter_reg_form=VoterRegForm()
    context={
        'login_form':login_form,
        'voter_reg_form':voter_reg_form,
        'work_fields_list':work_fields_list
    }
    return render(request,'index.html',context)