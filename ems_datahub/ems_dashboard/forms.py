from django import forms
from .models import Call, Agency, Town

class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
