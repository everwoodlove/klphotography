# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'website/home.html')

def pricing(request):
    return render(request, 'website/pricing.html')

def aboutme(request):
    return render(request, 'website/about-me.html')

def gallery(request):
    return render(request, 'website/gallery.html')

def contact(request):
    return render(request, 'website/contact.html')