
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Atividade, Equipamento, InstanciaEquipamento


class AtividadeListView(LoginRequiredMixin, generic.ListView):
    model = Atividade
    template_name = 'feed/feed_page.html'
    paginate_by = 10


class EquipamentoListView(generic.ListView):
    model = InstanciaEquipamento
    template_name = 'feed/lista_inventario.html'


class InstEquipamentoDetailView(generic.DetailView):
    model = InstanciaEquipamento
    template_name = "feed/detail_inventario.html"
