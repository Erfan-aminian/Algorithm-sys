from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import AlgorithmForm,FirstForm,create_dynamic_process_formset,DynamicForm
from .models import AlgorithmModel, DynamicProcessModel
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
                return redirect('home:count')
            elif selected=='3':
                return redirect('home:count')
            messages.success(request, 'you chioce', 'success')
            form.save()
        else:
            form = AlgorithmForm()
        return render(request, 'home/home.html', {'form': form})





class GetProcessCountView(View):
    def get(self, request):
        # نمایش فرم اولیه برای دریافت تعداد پردازش‌ها
        first_form = FirstForm()
        return render(request, 'home/count.html', {'form': first_form})

    def post(self, request):
        # پردازش داده‌های `FirstForm`
        first_form = FirstForm(request.POST)
        if first_form.is_valid():
            # دریافت تعداد پردازش‌ها از فیلد `field_count`
            field_count = first_form.cleaned_data['field_count']
            # ذخیره تعداد پردازش‌ها در سشن
            request.session['field_count'] = field_count
            # هدایت به ویوی داینامیک برای نمایش `Formset`
            return redirect('home:dynamic')  # باید نام URL ویو `DynamicProcessFormView` باشه

        return render(request, 'home/count.html', {'form': first_form})




class DynamicProcessView(View):
    def get(self, request):
        # دریافت تعداد پردازش‌ها از سشن
        field_count = request.session.get('field_count', 0)

        # ایجاد `Formset` داینامیک بر اساس تعداد پردازش‌ها
        ProcessFormSet = create_dynamic_process_formset(field_count=field_count)
        formset = ProcessFormSet(queryset=DynamicProcessModel.objects.none())  # برای ایجاد فرم‌های جدید

        return render(request, 'home/fcfs.html', {'formset': formset})

    def post(self, request):
        # دریافت تعداد پردازش‌ها از سشن
        field_count = request.session.get('field_count', 0)

        # ایجاد `Formset` داینامیک بر اساس تعداد پردازش‌ها
        ProcessFormSet = create_dynamic_process_formset(field_count=field_count)
        formset = ProcessFormSet(request.POST, queryset=DynamicProcessModel.objects.none())

        # پردازش داده‌های ارسالی از فرم‌ست
        if formset.is_valid():
            formset.save()  # ذخیره داده‌ها در پایگاه‌داده
            return redirect('home:sjf')
        # ریدایرکت یا نمایش موفقیت

        return render(request, 'home/fcfs.html', {'formset': formset})


class Fcfsview(View):
    def get(self, request):
        processes = list(DynamicProcessModel.objects.all().order_by('arrival_time'))

        if processes:
            waiting_times = []
            turnaround_times = []

            current_time = 0
            total_waiting_time = 0
            total_turnaround_time = 0

            process_data = []  # این لیست به جای result استفاده می‌شه

            for process in processes:
                if current_time < process.arrival_time:
                    current_time = process.arrival_time
                waiting_time = current_time - process.arrival_time
                waiting_times.append(waiting_time)

                current_time += process.burst_time
                turnaround_time = current_time - process.arrival_time
                turnaround_times.append(turnaround_time)

                total_waiting_time += waiting_time
                total_turnaround_time += turnaround_time

                # اضافه کردن داده‌ها به لیست process_data
                process_data.append({
                    'process_name': process.process_name,
                    'arrival_time': process.arrival_time,
                    'burst_time': process.burst_time,
                    'waiting_time': waiting_time,
                    'turnaround_time': turnaround_time,
                })

            avg_waiting_time = total_waiting_time / len(processes)
            avg_turnaround_time = total_turnaround_time / len(processes)
        else:
            avg_waiting_time = 0
            avg_turnaround_time = 0
            process_data = []

        context = {
            'process_data': process_data,  # ارسال لیست process_data به قالب
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        }

        return render(request, 'home/fcfs_result.html', context)


class SjfView(View):
    def get(self, request):
        # دریافت تعداد پردازش‌ها از سشن یا درخواست (در صورت نیاز می‌توان تغییر داد)
        process_count = request.session.get('process_count', None)

        if process_count is None:
            return HttpResponse("Error: Number of processes not specified.", status=400)

        # دریافت فقط تعداد مشخص‌شده از پردازش‌ها
        processes = list(DynamicProcessModel.objects.all().order_by('arrival_time')[:process_count])

        if processes:
            waiting_times = []
            turnaround_times = []

            current_time = 0
            total_waiting_time = 0
            total_turnaround_time = 0

            completed_processes = []
            process_data = []

            while len(completed_processes) < len(processes):
                # انتخاب پردازش‌های قابل اجرا (زمان ورود <= زمان فعلی)
                available_processes = [
                    process for process in processes if
                    process.arrival_time <= current_time and process not in completed_processes
                ]

                if available_processes:
                    # انتخاب پردازشی که زمان اجرای کوتاه‌تری داره
                    next_process = min(available_processes, key=lambda p: p.burst_time)

                    # محاسبه زمان انتظار
                    waiting_time = current_time - next_process.arrival_time
                    waiting_times.append(waiting_time)

                    # به‌روزرسانی زمان فعلی
                    current_time += next_process.burst_time

                    # محاسبه زمان بازگشت
                    turnaround_time = current_time - next_process.arrival_time
                    turnaround_times.append(turnaround_time)

                    # به‌روزرسانی مقادیر کل
                    total_waiting_time += waiting_time
                    total_turnaround_time += turnaround_time

                    # اضافه کردن به لیست پردازش‌های کامل‌شده
                    completed_processes.append(next_process)

                    # اضافه کردن داده‌ها به لیست process_data
                    process_data.append({
                        'process_name': next_process.process_name,
                        'arrival_time': next_process.arrival_time,
                        'burst_time': next_process.burst_time,
                        'waiting_time': waiting_time,
                        'turnaround_time': turnaround_time,
                    })
                else:
                    # اگر پردازشی برای اجرا وجود نداره، زمان فعلی رو به اولین پردازش بعدی منتقل کن
                    current_time = min(
                        process.arrival_time for process in processes if process not in completed_processes
                    )

            avg_waiting_time = total_waiting_time / len(processes)
            avg_turnaround_time = total_turnaround_time / len(processes)
        else:
            avg_waiting_time = 0
            avg_turnaround_time = 0
            process_data = []

        context = {
            'process_data': process_data,  # ارسال لیست process_data به قالب
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        }

        return render(request, 'home/sjf.html', context)

