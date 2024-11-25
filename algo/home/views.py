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
                return redirect('home:sjf')
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
            return redirect('home:fcfs')
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
    template_name = 'home/sjf.html'  # قالب HTML برای نمایش و پردازش

    def get(self, request):
        # اگر تعداد پردازش‌ها از قبل در سشن ذخیره شده بود، فرم داینامیک رو نمایش بده
        field_count = request.session.get('field_count', None)
        if field_count:
            formset = create_dynamic_process_formset(field_count=field_count)()
            return render(request, self.template_name, {'formset': formset, 'step': 2})

        # در غیر این صورت، فرم برای دریافت تعداد پردازش‌ها رو نمایش بده
        form = FirstForm()
        return render(request, self.template_name, {'form': form, 'step': 1})

    def post(self, request):
        if 'step' in request.POST and request.POST['step'] == '1':
            # مرحله اول: دریافت تعداد پردازش‌ها
            form = FirstForm(request.POST)
            if form.is_valid():
                field_count = form.cleaned_data['field_count']
                request.session['field_count'] = field_count  # ذخیره تعداد پردازش‌ها در سشن
                return redirect('home:sjf')
            return render(request, self.template_name, {'form': form, 'step': 1})

        elif 'step' in request.POST and request.POST['step'] == '2':
            # مرحله دوم: دریافت اطلاعات پردازش‌ها
            field_count = request.session.get('field_count', 0)
            formset = create_dynamic_process_formset(field_count)(request.POST)
            if formset.is_valid():
                # داده‌ها رو به صورت موقت از فرم داینامیک می‌گیریم، بدون ذخیره در دیتابیس
                processes = []
                for form in formset:
                    if form.cleaned_data:
                        process_name = form.cleaned_data['process_name']
                        arrival_time = form.cleaned_data['arrival_time']
                        burst_time = form.cleaned_data['burst_time']
                        processes.append(DynamicProcessModel(
                            process_name=process_name,
                            arrival_time=arrival_time,
                            burst_time=burst_time
                        )

