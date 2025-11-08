from django.shortcuts import render
from django.http import HttpResponse


def sey_hello(request):
    x = 1
    y = 2
    return render(request, "index.html")
