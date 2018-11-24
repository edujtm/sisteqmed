from django.shortcuts import render
from django.views import generic

from .models import Atividade


class ListaAtividadeView(generic.ListView):
    model = Atividade
    template_name = 'feed/feed_page.html'
    paginate_by = 15
