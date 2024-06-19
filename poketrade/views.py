from django.shortcuts import render
from django.urls import reverse_lazy

def homeView(request):
    ctx = {'title' : 'Home'}
    return render(request, template_name='base.html', context=ctx)
