from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import AlgorithmForm
from .models import AlgorithmModel
from django.contrib import messages
# Create your views here.


class HomeView(View):
    def get(self, request):
        form = AlgorithmForm()
        return render(request, 'home/home.html',{'form': form})
    def post(self, request):
        form = AlgorithmForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'you chioce', 'success')
        else:
            form = AlgorithmForm()
        return render(request, 'home/home.html',{'form': form})



