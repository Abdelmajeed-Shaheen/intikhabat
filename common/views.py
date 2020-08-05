from django.shortcuts import render
from users_management.forms import LoginForm
from voters_management.form import VoterRegForm
# Create your views here.
def home(request):
    login_form=LoginForm
    voter_reg_form=VoterRegForm()
    context={
        'login_form':login_form,
        'voter_reg_form':voter_reg_form
    }
    return render(request,'index.html',context)