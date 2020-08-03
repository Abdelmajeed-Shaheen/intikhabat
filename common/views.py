from django.shortcuts import render
from users_management.forms import LoginForm
# Create your views here.
def home(request):
    login_form=LoginForm
    # user=request.user
    # for value in user.first_name:
    #     print(value)
    # if hasattr(user, 'userprofile'):
    #     print("im candidate")
    # else :
    #     print("not candi")
    context={
        'login_form':login_form
    }
    return render(request,'index.html',context)