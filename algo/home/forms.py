from django import forms
from .models import AlgorithmModel,CountModel,FcfsProcessModel

class AlgorithmForm(forms.ModelForm):
    class Meta:
        model = AlgorithmModel
        fields = ('option',)
        widgets = {
            'option' : forms.RadioSelect
        }


class FirstForm(forms.Form):
    field_count = forms.IntegerField(label='Number of processes', min_value=1)


class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        field_count = kwargs.pop('field_count', 0)
        super(DynamicForm, self).__init__(*args, **kwargs)

        # اضافه کردن فیلدها بر اساس تعداد وارد شده در فرم اول
        for i in range(field_count):
            self.fields[f'arrival_time_{i}'] = forms.IntegerField(label=f'Arrival Time for Process {i + 1}')
            self.fields[f'burst_time_{i}'] = forms.IntegerField(label=f'Burst Time for Process {i + 1}')