from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import AlgorithmForm,CountAlgorithmForm, FcfsAlgorithmForm
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
    count_algo = CountAlgorithmForm
    fcfs_form = FcfsAlgorithmForm
    def get(self, request):
        return render(request, 'home/count.html', {'form':self.count_algo})

    def post(self, request):
        form = self.fcfs_form(request.POST)
        if form.is_valid():
            count_form = self.count_algo(request.POST)
            if count_form.is_valid():
                count = count_form.cleaned_data['count']
                self.fcfs_form(count=count)
        return render(request,'home/fcfs.html', {'form': form})













