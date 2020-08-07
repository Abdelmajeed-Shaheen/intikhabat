from django import forms 
from common.models import Address
from users_management.models import Candidate,WorkField

class VoterRegForm(forms.Form):
    first_name=forms.CharField(max_length=16,widget=forms.TextInput(
                                                    attrs={
                                                        'class':'form-control',
                                                        'placeholder':'الاسم الاول'
                                                    }
                                                    ))
    second_name=forms.CharField(max_length=16,widget=forms.TextInput(
                                                     attrs={
                                                         'class':'form-control',
                                                         'placeholder':'اسم الاب'
                                                     }   
                                                     ))
    third_name=forms.CharField(max_length=16,widget=forms.TextInput(
                                                      attrs={
                                                            'class':'form-control',
                                                             'placeholder':'اسم الجد'                                                              
                                                        }
                                                        ))
    last_name=forms.CharField(max_length=16,widget=forms.TextInput(
                                                    attrs={
                                                        'class':'form-control',
                                                        'placeholder':'الاسم العائلة'
                                                    }
                                                    ))
    mobile_number=forms.CharField(max_length=15,widget=forms.TextInput(
                                                    attrs={
                                                        'class':'form-control',
                                                        'placeholder':'رقم الهاتف'
                                                    }
                                                    ))
    whatsapp_number=forms.CharField(max_length=15,widget=forms.TextInput(
                                                    attrs={
                                                        'class':'form-control',
                                                        'placeholder':'رقم الواتساب'
                                                    }
                                                    ))
    email=forms.CharField(max_length=15,widget=forms.EmailInput(
                                                    attrs={
                                                        'class':'form-control',
                                                        'placeholder':'البريد الالكتروني'
                                                    }
                                                    ))                                                
    dob=forms.DateField(input_formats='%Y,%m,%d',widget=forms.SelectDateWidget(
                                                                            years=range(1940, 2003,),
                                                                            empty_label=("السنة", "الشهر", "اليوم")
                                                                            ))
    GENDER_CHOICES=(('male', 'ذكر'),('female', 'انثى'),)
    gender=forms.ChoiceField(choices=GENDER_CHOICES)

    address=forms.ModelChoiceField(queryset=Address.objects.all())
    work=forms.ModelChoiceField(queryset=WorkField.objects.all())



class VoterUpdateForm(forms.Form):

    candidate=forms.ModelChoiceField(queryset=Candidate.objects.all())
    VOTE_STATUS_CHOICES=[
                ('Voting','مؤيد'),
                ('Not_sure','متردد'),
                ('Not_voting','ممتنع')
                ]
    vote_status=forms.ChoiceField(choices=VOTE_STATUS_CHOICES,widget=forms.Select(attrs={'class':'form-control'}))

    