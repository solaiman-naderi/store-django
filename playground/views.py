from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product


def sey_hello(request):
    try:
        query_set = Product.objects.get(pk=81)
        print(query_set)
    except:
        pass

    return render(request, "index.html")
