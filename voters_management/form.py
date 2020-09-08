from django import forms 
from common.models import Address
from users_management.models import Candidate,WorkField



MONTHS = {
    1:('1'), 2:('2'), 3:('3'), 4:('4'),
    5:('5'), 6:('6'), 7:('7'), 8:('8'),
    9:('9'), 10:('10'), 11:('11'), 12:('12')
}
class VoterRegForm(forms.Form):
    first_name=forms.CharField(max_length=16,widget=forms.TextInput(
                                                    attrs={
                                                        'class':'form-control',
                                                        'placeholder':'الاسم الاول',
                                                        "data-field-name":'الاسم الاول',
                                                    }
                                                    ))
    second_name=forms.CharField(max_length=16,widget=forms.TextInput(
                                                     attrs={
                                                         'class':'form-control',
                                                         'placeholder':'اسم الاب',
                                                         "data-field-name":'اسم الاب'
                                                     }   
                                                     ))
    third_name=forms.CharField(max_length=16,widget=forms.TextInput(
                                                      attrs={
                                                            'class':'form-control',
                                                             'placeholder':'اسم الجد',
                                                             "data-field-name":'اسم الجد'                                                              
                                                        }
                                                        ))
    last_name=forms.CharField(max_length=16,widget=forms.TextInput(
                                                    attrs={
                                                        'class':'form-control',
                                                        'placeholder':'الاسم العائلة',
                                                        "data-field-name":'الاسم العائلة'
                                                    }
                                                    ))
    mobile_number=forms.CharField(max_length=15,widget=forms.TextInput(
                                                    attrs={
                                                        'class':'form-control',
                                                        'placeholder':'رقم الهاتف',
                                                        "data-field-name":'رقم الهاتف'
                                                        
                                                    }
                                                    ))
    whatsapp_number=forms.CharField(max_length=10,widget=forms.TextInput(

                                                    attrs={
                                                        'class':'form-control',
                                                        'placeholder':'رقم الواتساب',
                                                        "data-field-name":'رقم الواتساب'
                                                        
                                                    }
                                                    ))
    email=forms.CharField(widget=forms.EmailInput(
                                                    attrs={
                                                        'class':'form-control',
                                                        'placeholder':'البريد الالكتروني',
                                                        "data-field-name":'البريد الالكتروني'
                                                    }
                                                    ))                                                
    dob=forms.DateField(input_formats='%Y-%m-%d',widget=forms.SelectDateWidget(
                                                    years=range(1940, 2004),
                                                    months=MONTHS,
                                                    empty_label=("السنة","الشهر", "اليوم"),
                                                    
                                                    ))
    GENDER_CHOICES=(('Male', 'ذكر'),('Female', 'انثى'),)
    gender=forms.ChoiceField(choices=GENDER_CHOICES)
    work=forms.ModelChoiceField(queryset=WorkField.objects.all(),widget=forms.Select(attrs={'class':'form-control m-2'}))
    identifier=forms.CharField(widget=forms.TextInput(
                                                    attrs={
                                                        'class':'form-control',
                                                        'placeholder':'الرقم الانتخابي للمعرف (ان وجد)'
                                                    }
                                                    ))

class VoterUpdateForm(forms.Form):

    candidate=forms.ModelChoiceField(queryset=Candidate.objects.all())
    VOTE_STATUS_CHOICES=[
                ('Voting','مؤيد'),
                ('Not_sure','متردد'),
                ('Not_voting','ممتنع')
                ]
    vote_status=forms.ChoiceField(choices=VOTE_STATUS_CHOICES,widget=forms.Select(attrs={'class':'form-control'}))

    