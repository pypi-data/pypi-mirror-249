from django.conf import settings
from django.forms import ModelForm, DateInput, ValidationError
from django.forms.fields import ChoiceField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django_bookdates.models import Timespan


class TimespanForm(ModelForm):
    class Meta:
        model = Timespan
        fields = ['start', 'end', 'title', 'body']
        widgets = {
                'start': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'end': DateInput(attrs={'type': 'date', 'class': 'form-control'})}

    def __init__(self, calendar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if choices := getattr(settings, "CALENDAR_CHOICES", {}).get(calendar.slug):
            choices = list(zip(choices, choices))
            choices.append(('', '-----'))
            self.fields["title"] = ChoiceField(choices=choices)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        if start > end:
            raise ValidationError("'start' date cannot be later than 'end' date.")
        return cleaned_data
