from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Atividade(models.Model):
    inicio = models.DateTimeField(default=timezone.now)
    finalizado = models.DateTimeField(null=True)
    justificativa = models.TextField(max_length=500, help_text='Justificativa para atividades não finalizadas',
                                     null=True)
    concluido = models.BooleanField(default=False)
    responsavel = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                    limit_choices_to={'groups__name__in': ['administrador', 'profissional da saude']})

    inst_equipamento = models.ForeignKey('InstanciaEquipamento', null=True, on_delete=models.SET_NULL)
    defeito = models.CharField(max_length=150, default="Sem descrição do defeito",
                               help_text='Breve descrição do defeito do equipamento. (máx. 150 caracteres)')

    PRIORIDADES = (
        (1, 'Baixa'),
        (2, 'Media'),
        (3, 'Alta'),
        (4, 'Urgente'),
    )

    prioridade = models.IntegerField(choices=PRIORIDADES, default=2)

    class Meta:
        ordering = ['inicio']
        permissions = (("can_add_status", "Adicionar novo status à atividade"),
                       ('can_finish_activity', "Permissão para concluir atividade"),
                       ('can_create_activity', 'Permissão para cadastrar atividade'),)

    def __str__(self):
        return f"Ordem de servico: {self.id}"

    def get_tempo_de_manutencao(self):
        if self.concluido:
            return self.finalizado - self.inicio
        return timezone.now() - self.inicio

    def concluir(self, just, concluido):
        instance = Atividade.objects.get(pk=self.pk)
        instance.concluido = concluido
        instance.finalizado = timezone.now()
        instance.justificativa = just
        instance.status_set.create(descricao="atividade concluida")
        instance.save()


class Status(models.Model):
    data = models.DateTimeField(default=timezone.now)
    descricao = models.CharField(max_length=150, help_text='Breve descricao do estado atual da atividade')

    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f'{self.descricao} em {self.data}'


class Equipamento(models.Model):
    nome = models.CharField(max_length=150, help_text="Nome do equipamento")
    descricao = models.TextField(max_length=500, help_text="Descricao das caracteristicas do equipamento",
                                 verbose_name="Descrição")

    class Meta:
        permissions = (('can_create_equipamento', 'Criar novo equipamento'), )

    def __str__(self):
        return self.nome


class InstanciaEquipamento(models.Model):
    num_de_serie = models.AutoField(primary_key=True)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)

    setor = models.ForeignKey('Setor', null=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (('can_add_inventario', 'Adicionar equipamento ao inventario'), )

    def __str__(self):
        return f"{self.equipamento} - N° de serie: {self.num_de_serie}"


class Setor(models.Model):
    nome = models.CharField(max_length=150, help_text="Nome do setor (máx. 150 caracteres)")
    telefone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                    message="Telefone deve ser digitado no seguinte formato: '+999999999'. "
                                            "Ate 15 caracteres sao permitidos.")
    telefone = models.CharField(validators=[telefone_regex], max_length=17, blank=True)

    def __str__(self):
        return self.nome
