from django import forms
from .models import AlgorithmModel,DynamicProcessModel
from django.forms import modelformset_factory

class AlgorithmForm(forms.ModelForm):
    class Meta:
        model = AlgorithmModel
        fields = ('option',)
        widgets = {
            'option' : forms.RadioSelect
        }


class FirstForm(forms.Form):
    field_count = forms.IntegerField(label='Number of processes', min_value=1)

class DynamicForm(forms.ModelForm):
        class Meta:
            model = DynamicProcessModel
            fields = ('process_name', 'arrival_time', 'burst_time')


def create_dynamic_process_formset(field_count=0):
    ProcessFormSet = modelformset_factory(
        DynamicProcessModel,
        form = DynamicForm,
        extra=field_count
    )
    return ProcessFormSet



