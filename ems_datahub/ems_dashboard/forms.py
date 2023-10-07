from django import forms
from .models import Call

class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class DataImportForm(forms.Form):
    data_file = forms.FileField(label='Select a file')