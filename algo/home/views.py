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
        form = FirstForm()
        return render(request, 'home/count.html', {'form': form})

    def post(self, request):
        # بررسی اینکه آیا فرم اول ارسال شده
        if 'field_count' in request.POST:
            first_form = FirstForm(request.POST)
            if first_form.is_valid():
                field_count = first_form.cleaned_data['field_count']
                print(f'First Form is valid. Field Count: {field_count}')
                # ساخت فرم داینامیک با تعداد فیلد مشخص
                dynamic_form = DynamicForm(field_count=field_count)
                return render(request, 'home/fcfs.html', {'form': dynamic_form, 'field_count': field_count})
            else:
                print('First Form is not valid.')
                print(first_form.errors)

        # بررسی اینکه آیا فرم دوم ارسال شده
        else:
            field_count = int(request.POST.get('field_count', 0))
            dynamic_form = DynamicForm(request.POST, field_count=field_count)

            # چاپ مقادیر دریافتی فرم دوم برای اشکال‌زدایی
            print(f'Dynamic Form data: {request.POST}')
            print(f'Field count: {field_count}')

            # اطمینان از معتبر بودن فرم
            if dynamic_form.is_valid():
                print('Dynamic Form is valid.')
                # پردازش فرم دوم
                processes = []
                for i in range(field_count):
                    arrival_time = int(request.POST.get(f'arrival_time_{i}'))
                    burst_time = int(request.POST.get(f'burst_time_{i}'))
                    processes.append((arrival_time, burst_time))

                # مرتب‌سازی پردازش‌ها بر اساس زمان ورود
                processes.sort(key=lambda x: x[0])

                # الگوریتم FCFS
                start_time = 0
                results = []
                for idx, (arrival_time, burst_time) in enumerate(processes):
                    start_time = max(start_time, arrival_time)
                    finish_time = start_time + burst_time
                    wait_time = start_time - arrival_time
                    turnaround_time = finish_time - arrival_time
                    results.append({
                        'process': idx + 1,
                        'arrival_time': arrival_time,
                        'burst_time': burst_time,
                        'start_time': start_time,
                        'finish_time': finish_time,
                        'wait_time': wait_time,
                        'turnaround_time': turnaround_time,
                    })
                    start_time = finish_time

                # ارسال نتایج به قالب جداگانه
                return render(request, 'home/fcfs_result.html', {'results': results})
            else:
                print('Dynamic Form is not valid.')
                print(dynamic_form.errors)
                # اگر فرم نامعتبر بود، دوباره به صفحه `fcfs.html` برمی‌گردد
                return render(request, 'home/fcfs.html', {'form': dynamic_form, 'field_count': field_count})

        # اگر هیچ فرمی ارسال نشده باشد، فرم اول را نشان می‌دهیم
        return render(request, 'home/count.html', {'form': FirstForm()})


