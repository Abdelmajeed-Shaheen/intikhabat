from django import forms 

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
    dob=forms.DateField(input_formats='%Y,%m,%d',widget=forms.SelectDateWidget())