
from django.shortcuts import render, redirect
from django.views import generic

from .models import Atividade, Equipamento, InstanciaEquipamento


class AtividadeListView(generic.ListView):
    model = Atividade
    template_name = 'feed/feed_page.html'
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(AtividadeListView, self).get(request, **kwargs)
        return redirect('home-page')


class EquipamentoListView(generic.ListView):
    model = InstanciaEquipamento
    template_name = 'feed/lista_inventario.html'


# TODO adicionar view para detalhes do equipamento