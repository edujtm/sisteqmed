
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.AtividadeListView.as_view(), name='index-page'),
    path("inventario/", views.EquipamentoListView.as_view(), name='inventario-list'),
    path('inventario/create/', views.CriarInstanciaEquipamentoView.as_view(), name='inventario-create'),
    path("inventario/<int:pk>", views.InstEquipamentoDetailView.as_view(), name='inventario-detail'),
    path('atividade/<int:pk>/confirm/', views.confirmar_conclusao_atividade, name='confirm-conclude'),
    path('atividade/create/', views.CriarAtividadeView.as_view(), name='create-atividade'),
    path('equipamento/create/', views.CriarEquipamentoView.as_view(), name='equipamento-create'),
]