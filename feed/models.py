from django.db import models
from django.utils import timezone


class Atividade(models.Model):
    inicio = models.DateTimeField(default=timezone.now)
    justificativa = models.TextField(max_length=200, help_text='Justificativa para atividades não finalizadas',
                                     null=True)
    concluido = models.BooleanField()

    PRIORIDADES = (
        (1, 'Baixa'),
        (2, 'Media'),
        (3, 'Alta'),
        (4, 'Urgente'),
    )

    def get_tempo_de_manutencao(self):
        return timezone.now() - self.inicio
