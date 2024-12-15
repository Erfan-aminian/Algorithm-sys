from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.generic import FormView

from .forms import AlgorithmForm,FirstForm,create_dynamic_process_formset,DynamicForm, QuantumForm
from .models import AlgorithmModel, DynamicProcessModel, QuantumModel
from django.contrib import messages
from .algorithm import SJFAlgorithm, SRTAlgorithm, RRAlgorithm

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
            if selected == '1':
                return redirect('home:count')
            elif selected == '2':
                return redirect('home:rr')
            elif selected == '3':
                return redirect('home:sjf')
            elif selected == '4':
                return redirect('home:srt')
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

        return render(request, 'home/dynamic.html', {'formset': formset})

    def post(self, request):
        DynamicProcessModel.objects.all().delete()
        # دریافت تعداد پردازش‌ها از سشن
        field_count = request.session.get('field_count', 0)

        # ایجاد `Formset` داینامیک بر اساس تعداد پردازش‌ها
        ProcessFormSet = create_dynamic_process_formset(field_count=field_count)
        formset = ProcessFormSet(request.POST, queryset=DynamicProcessModel.objects.none())

        # پردازش داده‌های ارسالی از فرم‌ست
        if formset.is_valid():
            formset.save()  # ذخیره داده‌ها در پایگاه‌داده
            return redirect('home:home')
        # ریدایرکت یا نمایش موفقیت

        return render(request, 'home/dynamic.html', {'formset': formset})

class QuantumView(View):
    def get(self, request):
        form = QuantumForm()
        return render(request, 'home/quantum.html', {'form': form })

    def post(self, request):
        QuantumModel.objects.all().delete()
        form = QuantumForm(request.POST)
        if form.is_valid():
            form.save()  # ذخیره فرم در پایگاه داده
            return redirect('home:rr')  # هدایت به صفحه موفقیت
        return render(request, 'home/quantum.html', {'form': form})


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
    def get(self, request, *args, **kwargs):
        # دریافت داده‌ها از پایگاه‌داده
        processes = list(
            DynamicProcessModel.objects.values("id", "arrival_time", "burst_time")
        )

        # اجرای الگوریتم
        sjf = SJFAlgorithm(processes)
        sjf.execute()
        results = sjf.get_results()

        # بازگشت نتایج به صورت JSON
        return render(request, 'home/sjf.html', {'results': results})

class SrtView(View):
    def get(self, request, *args, **kwargs):
        processes = []
        dynamic_processes = DynamicProcessModel.objects.all()  # دریافت تمام رکوردها

        for process in dynamic_processes:
            processes.append({
                'process_name': process.process_name,
                'arrival_time': process.arrival_time,
                'burst_time': process.burst_time
            })
        # اجرای الگوریتم SRT
        srt_algo = SRTAlgorithm(processes)
        result = srt_algo.execute()

        return render(request, 'home/srt.html', {'result': result})


class RoundRobinView(View):
    def get(self, request, *args, **kwargs):
        processes = []
        dynamic_processes = DynamicProcessModel.objects.all()
        quantum = QuantumModel.objects.all()

        if not dynamic_processes.exists():
            return render(request, 'home/rr.html', {'result': [], 'error': 'No processes found in the database.'})

        # دریافت Time Quantum از اولین فرآیند
        time_quantum = quantum.first().quantum

        # جمع‌آوری داده‌های فرآیندها
        for process in dynamic_processes:
            processes.append({
                'process_name': process.process_name,
                'arrival_time': process.arrival_time,
                'burst_time': process.burst_time
            })

        # اجرای الگوریتم RR
        rr_algo = RRAlgorithm(processes, time_quantum)
        result = rr_algo.execute()

        # ارسال نتایج به قالب
        return render(request, 'home/rr.html', {'result': result, 'time_quantum': time_quantum})