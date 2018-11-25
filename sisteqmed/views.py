
from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return redirect('index-page')
    return render(request, 'sisteqmed/base_generic.html')
