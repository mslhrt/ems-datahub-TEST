from django import forms
from datetime import datetime
from .models import Call

class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        input_date = cleaned_data.get("date")
        input_time = cleaned_data.get("time")
        now = datetime.now()
        input_datetime = datetime.combine(input_date, input_time)

        if input_datetime > now:
            raise forms.ValidationError("The date/time cannot be in the future.")

        return cleaned_data

class DataImportForm(forms.Form):
    data_file = forms.FileField(label='Select a file')
