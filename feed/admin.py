from django.contrib import admin

from .models import Atividade, Equipamento, InstanciaEquipamento, Setor, Status


admin.site.register(Status)


class StatusInline(admin.TabularInline):
    model = Status
    extra = 0


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'inicio', 'concluido', 'responsavel')
    list_filter = ('concluido', 'responsavel__username', 'prioridade')

    fieldsets = (
        ('Descricao',
         {'fields': ['inst_equipamento', 'responsavel', 'prioridade']}),
        ('Status',
         {'fields': ['inicio', 'concluido', 'defeito']})
    )

    inlines = [StatusInline]


@admin.register(InstanciaEquipamento)
class InstanciaEquipamentoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'setor')
    list_filter = ('setor', )


class InstanceEquipamentoInline(admin.TabularInline):
    model = InstanciaEquipamento


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):

    inlines = [InstanceEquipamentoInline]


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone')
