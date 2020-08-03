from django import forms
from .models import Comittee

class CreateComitteeForm(forms.ModelForm):
    class Meta:
        model=Comittee
       
        fields=['name','description','is_active','address','candidate']

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'اسم اللجنة'}))
    description=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'شرح مبسط عن اللجنة','rows':5}))
    is_active=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    
    