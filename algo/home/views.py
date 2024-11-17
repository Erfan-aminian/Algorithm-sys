from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import AlgorithmForm,FirstForm, DynamicForm
from .models import AlgorithmModel
from django.contrib import messages
from .fcfs_scheduler import FcfsScheduler  # اضافه کردن کلاس FcfsScheduler

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
        form = FirstForm()
        return render(request, 'home/count.html', {'form': form})

    def post(self, request):
        # بررسی اینکه آیا فرم اول ارسال شده
        if 'field_count' in request.POST:
            first_form = FirstForm(request.POST)
            if first_form.is_valid():
                field_count = first_form.cleaned_data['field_count']
                print(f"First Form is valid. Field Count: {field_count}")  # نمایش تعداد فیلدها
                dynamic_form = DynamicForm(field_count=field_count)
                return render(request, 'home/fcfs.html', {'form': dynamic_form, 'field_count': field_count})
            else:
                print('First Form is not valid.')
                print(first_form.errors)
        else:
            # بررسی اینکه آیا فرم دوم ارسال شده
            field_count = int(request.POST.get('field_count', 0))
            dynamic_form = DynamicForm(request.POST, field_count=field_count)

            if dynamic_form.is_valid():
                print('Dynamic Form is valid.')
                processes = []
                for i in range(field_count):
                    arrival_time = int(request.POST.get(f'arrival_time_{i}'))
                    burst_time = int(request.POST.get(f'burst_time_{i}'))
                    processes.append((arrival_time, burst_time))

                print(f"Processes Data: {processes}")  # نمایش داده‌های پردازش‌ها

                # استفاده از کلاس FcfsScheduler برای محاسبه نتایج
                scheduler = FcfsScheduler(processes)
                scheduler.calculate()  # محاسبات الگوریتم FCFS
                results = scheduler.get_results()  # گرفتن نتایج

                print(f"Results: {results}")  # نمایش نتایج محاسبات
                return render(request, 'home/fcfs_result.html', {'results': results})
            else:
                print('Dynamic Form is not valid.')
                print(dynamic_form.errors)
                return render(request, 'home/fcfs.html', {'form': dynamic_form, 'field_count': field_count})

        return render(request, 'home/count.html', {'form': FirstForm()})
