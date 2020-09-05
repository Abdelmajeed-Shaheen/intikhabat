from django import forms
from .models import Comittee
from users_management.models import ComitteeMember,UserProfile
from tasks.models import ComitteeTask   
class CreateComitteeForm(forms.ModelForm):
    class Meta:
        model=Comittee
       
        fields=['name','description','is_active','address','candidate','address_description']

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'اسم اللجنة'}))
    description=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'شرح مبسط عن اللجنة','rows':5}))
    is_active=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    address_description=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'عنوان مقر اللجنة','rows':2}))    


class UpdateCmForm(forms.ModelForm):

    class Meta:
        model=ComitteeMember
        fields=['is_manager','comittee']

    comittee=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'اسم اللجنة'}))
    is_manager=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))


class ComitteeTaskForm(forms.ModelForm):

    class Meta:
        model=ComitteeTask
        fields=["description","notes","is_complete","comittee","title"]
    description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'وصف المهمة'}))
    notes=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'ملاحظات'}))
    title=forms.CharField( max_length=255, required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'عنوان المهمة'}))
    
    def __init__(self, candidate=None, *args, **kwargs):
        super(ComitteeTaskForm, self).__init__(*args, **kwargs)
        self.fields['comittee'].queryset = Comittee.objects.all().filter(candidate=candidate,is_active=True)
       
        
