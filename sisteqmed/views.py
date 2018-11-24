
from django.shortcuts import render


def index(request):
    return render(request, 'sisteqmed/base_generic.html')
