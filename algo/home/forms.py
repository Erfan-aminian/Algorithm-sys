from django import forms
from .models import AlgorithmModel,CountModel,FcfsProcessModel

class AlgorithmForm(forms.ModelForm):
    class Meta:
        model = AlgorithmModel
        fields = ('option',)
        widgets = {
            'option' : forms.RadioSelect
        }

class CountAlgorithmForm(forms.Form):
    class Meta:
        model = CountModel
        fields = ('count',)
        widgets = {
            'count': forms.NumberInput(attrs=
                                       {'class':'form-control', 'placeholder':'Number of processes', 'min':1, 'max':9})
        }


class FcfsAlgorithmForm(forms.Form):
    class Meta:
        model = CountModel
        fields = ()

    def __init__(self, *args, **kwargs):
        count = kwargs.pop('count', 1)
        super(CountAlgorithmForm, self).__init__(*args, **kwargs)
        for i in range(count):
            self.fields[f'process_{i + 1}'] = forms.IntegerField(
                label=f'Execution Time for Process {i + 1}',
                min_value=1,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': f'Execution time for process {i + 1}'
                })
            )




