from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HtmlResponse("Hello, world. You're at the home page.") 