
from django.urls import path
from . import views

urlpatterns = [
    path("", views.AtividadeListView.as_view(), name='index-page'),
    path("equipamentos/", views.EquipamentoListView.as_view(), name='equipamento-list'),
]