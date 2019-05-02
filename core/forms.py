from django import forms
from datetime import datetime
from .models import Dayoff


class DateInput(forms.DateInput):
    input_type = 'date'

class DayoffForm(forms.ModelForm):
    reason = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Dayoff
        exclude = ['create_by', 'approve_status']
        widgets = {
            'date_start': DateInput(),
            'end_date' : DateInput()
        }

    def clean_date_start(self):
        data = self.cleaned_data.get('date_start')

        if data < datetime.now().date():
            raise forms.ValidationError('ไม่สามารถเลือกวันในอดีตได้')
        return data

    def clean_end_date(self):
        data = self.cleaned_data.get('end_date')

        if data < datetime.now().date():
            raise forms.ValidationError('ไม่สามารถเลือกวันในอดีตได้')
        return data

    def clean(self):
        clean = super().clean()
        day1 = clean.get('date_start')
        day2 = clean.get('end_date')
        if day2 < day1:
            self.add_error('end_date', 'วันที่ไม่ถูกต้อง')


