from django import forms
from .models import Case

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = '__all__'
        widgets = {
            'institution_date': forms.DateInput(attrs={'type': 'date'}),
            'hearing_date': forms.DateInput(attrs={'type': 'date'}),
            'disposal_date': forms.DateInput(attrs={'type': 'date'}),
        }
