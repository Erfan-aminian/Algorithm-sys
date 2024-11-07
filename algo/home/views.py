from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
# Create your views here.


class HomeView(View):
    def get(self, request):
        return render(request, 'home/home.html')
