
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect

from .models import Atividade, Equipamento, InstanciaEquipamento, Status
from .forms import ConfirmarAtividadeForm, CadastrarEquipamentoForm, AddStatusForm


class AtividadeListView(generic.ListView, LoginRequiredMixin, FormMixin):
    model = Atividade
    template_name = 'feed/feed_page.html'
    paginate_by = 10
    form_class = AddStatusForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.form_class()

        return generic.ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            pk = request.POST.get('atividade-id')
            atv = get_object_or_404(Atividade, pk=pk)
            desc = self.form.cleaned_data['descricao']
            Status.objects.create(descricao=desc, atividade=atv)

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AtividadeListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context


class EquipamentoListView(generic.ListView):
    model = InstanciaEquipamento
    template_name = 'feed/lista_inventario.html'


class InstEquipamentoDetailView(generic.DetailView):
    model = InstanciaEquipamento
    template_name = "feed/detail_inventario.html"


@permission_required('feed.can_finish_activity')
def confirmar_conclusao_atividade(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)

    if request.method == 'POST':

        form = ConfirmarAtividadeForm(request.POST)

        if form.is_valid():
            justificativa = form.cleaned_data['justificativa']
            concluido = form.cleaned_data['concluido']
            atividade.concluir(justificativa, concluido)
            return HttpResponseRedirect(reverse('index-page'))
    else:
        form = ConfirmarAtividadeForm()

    context = {
        'form': form,
        'atividade': atividade,
    }
    return render(request, 'feed/confirm_conclude.html', context)


class CriarAtividadeView(PermissionRequiredMixin, CreateView):
    model = Atividade
    fields = ['responsavel', 'inst_equipamento', 'defeito', 'prioridade']
    success_url = reverse_lazy('index-page')
    permission_required = ('feed.can_create_activity', )


class CriarInstanciaEquipamentoView(PermissionRequiredMixin, CreateView):
    model = InstanciaEquipamento
    template_name = 'feed/add_inventario_form.html'
    fields = '__all__'
    permission_required = ('feed.can_add_inventario', )
    success_url = reverse_lazy('inventario-list')


class CriarEquipamentoView(PermissionRequiredMixin, CreateView):
    model = Equipamento
    form_class = CadastrarEquipamentoForm
    template_name = 'feed/criar_equipamento_form.html'
    permission_required = ('feed.can_create_equipamento', )
    success_url = reverse_lazy('inventario-list')
