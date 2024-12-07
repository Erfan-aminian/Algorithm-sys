# forms.py
from django import forms
from .models import AlgorithmModel, DynamicProcessModel
from django.forms import modelformset_factory

class AlgorithmForm(forms.ModelForm):
    class Meta:
        model = AlgorithmModel
        fields = ('option',)
        widgets = {
            'option': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اگر الگوریتم Round Robin انتخاب شده باشد، فیلد زمان کوانتوم را اضافه کن
        if self.instance and self.instance.option == 'RR':
            self.fields['quantum'] = forms.IntegerField(min_value=1, required=True, label='Quantum Time', initial=5)
        else:
            # اگر انتخاب دیگری باشد، فیلد quantum را مخفی کن
            self.fields.pop('quantum', None)


class FirstForm(forms.Form):
    field_count = forms.IntegerField(label='Number of processes', min_value=1)


class DynamicForm(forms.ModelForm):
    class Meta:
        model = DynamicProcessModel
        fields = ('process_name', 'arrival_time', 'burst_time', 'priority')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اگر الگوریتم Round Robin انتخاب شده باشد، فیلد quantum را نشان بده
        if 'quantum' in kwargs.get('initial', {}):
            self.fields['quantum'] = forms.IntegerField(min_value=1, required=True, label='Quantum Time', initial=5)


def create_dynamic_process_formset(field_count=0):
    ProcessFormSet = modelformset_factory(
        DynamicProcessModel,
        form=DynamicForm,
        extra=field_count
    )
    return ProcessFormSet
