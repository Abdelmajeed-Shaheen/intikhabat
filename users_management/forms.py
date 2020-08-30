from django import forms
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users_management.models import UserProfile

GENDER_CHOICES=[
                ('ذكر','ذكر'),
                ('انثى','انثى')
                ]

class LoginForm(forms.Form):
    username = forms.CharField(
    				widget=forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "رقم الهاتف"
                    	}
                    )
    	)
    password = forms.CharField(
    				widget=forms.PasswordInput(
                    attrs={
                        "class": "form-control", 
                        "placeholder": "كلمة السر"
                    	}
                    )
    	)

class CandidateLoginForm(forms.Form):
    candidate_username = forms.CharField(
    				widget=forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "رقم الهاتف"
                    	}
                    )
    	)
    candidate_password = forms.CharField(
    				widget=forms.PasswordInput(
                    attrs={
                        "class": "form-control", 
                        "placeholder": "كلمة السر"
                    	}
                    )
    	)



class SignUpForm(forms.Form):
    first_name = forms.CharField(
                                 widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "الاسم الاول"
                                            }
                                        )
    )
    last_name = forms.CharField(
                                widget=forms.TextInput(
                                        attrs={
                                                "class": "form-control",
                                                "placeholder": "الاسم العائلة"
                                                }
                                            )
                                
    )

    middle_name=forms.CharField(
                                widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "اسم الاب"
                                            }
                                        )
    )
    third_name=forms.CharField(
                                widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "اسم الجد"
                                            }
                                        )
    )
    mobile_number=forms.CharField(
                                   widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "رقم الهاتف"
                                            }
                                        )
    
    )
    whatsapp_number=forms.CharField(
                                     widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "رقم الواتساب"
                                            }
                                        )
    )
    email=forms.EmailField( widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "البريد الالكتروني"
                                            }
                                        ))
    date_of_birth=forms.DateField()
    is_manager=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))


class CampaignAdminCreateForm(forms.Form):
    ca_first_name = forms.CharField(
                                 widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "الاسم الاول"
                                            }
                                        )
    )
    ca_last_name = forms.CharField(
                                widget=forms.TextInput(
                                        attrs={
                                                "class": "form-control",
                                                "placeholder": "الاسم العائلة"
                                                }
                                            )
                                
    )

    ca_middle_name=forms.CharField(
                                widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "اسم الاب"
                                            }
                                        )
    )
    ca_third_name=forms.CharField(
                                widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "اسم الجد"
                                            }
                                        )
    )
    ca_mobile_number=forms.CharField(
                                   widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "رقم الهاتف"
                                            }
                                        )
    
    )
    ca_whatsapp_number=forms.CharField(
                                     widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "رقم الواتساب"
                                            }
                                        )
    )
    ca_email=forms.EmailField( widget=forms.TextInput(
                                        attrs={
                                            "class": "form-control",
                                            "placeholder": "البريد الالكتروني"
                                            }
                                        ))
    ca_date_of_birth=forms.DateField()
    