from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import AlgorithmForm,FirstForm, DynamicForm
from .models import AlgorithmModel
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.


class HomeView(View):
    def get(self, request):
        form = AlgorithmForm()
        return render(request, 'home/home.html', {'form': form})
    def post(self, request):
        form = AlgorithmForm(request.POST)
        if form.is_valid():
            selected = form.cleaned_data['option']
            if selected=='1':
                return redirect('home:fcfs')
            messages.success(request, 'you chioce', 'success')
            form.save()
        else:
            form = AlgorithmForm()
        return render(request, 'home/home.html', {'form': form})
class FcfsView(View):
    def get(self, request):
        first_form = FirstForm()
        return render(request, 'home/fcfs.html', {'form': first_form})

    def post(self, request):
        if request.method == 'POST':
            # بررسی اینکه آیا فرم اول ارسال شده
            if 'field_count' in request.POST:
                first_form = FirstForm(request.POST)
                if first_form.is_valid():
                    field_count = first_form.cleaned_data['field_count']
                    # ساخت فرم داینامیک با تعداد فیلد مشخص
                    dynamic_form = DynamicForm(field_count=field_count)
                    return render(request, 'home/fcfs.html', {'form': dynamic_form})

            # بررسی اینکه آیا فرم دوم ارسال شده
            else:
                dynamic_form = DynamicForm(request.POST, field_count=int(request.POST.get('field_count', 0)))
                if dynamic_form.is_valid():
                    # پردازش فرم دوم
                    return redirect('success')

        else:
            first_form = FirstForm()
            return render(request, 'home/count.html', {'form': first_form})













