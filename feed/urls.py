
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListaAtividadeView.as_view(), name='index-page')
]