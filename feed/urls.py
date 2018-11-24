
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.AtividadeListView.as_view(), name='index-page'),
    path("inventario/", views.EquipamentoListView.as_view(), name='inventario-list'),
    path("inventario/<int:pk>", views.InstEquipamentoDetailView.as_view(), name='inventario-detail')
]