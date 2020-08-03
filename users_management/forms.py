from django import forms
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

GENDER_CHOICES=[
                ('ذكر','ذكر'),
                ('انثى','انثى')
                ]

class LoginForm(forms.Form):
    username = forms.CharField(
    				widget=forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "رقم الهاتف / اسم المستخدم"
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


 