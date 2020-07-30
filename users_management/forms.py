from django import forms

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
