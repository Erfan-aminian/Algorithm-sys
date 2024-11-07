from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import AlgorithmForm
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
        return HttpResponse('this page for fcfs algorithm.')




