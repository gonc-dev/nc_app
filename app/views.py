from django.shortcuts import render
from django.views.generic import TemplateView
import os

# Create your views here.
class Home(TemplateView):
    template_name = os.path.join('app', 'index.html')




