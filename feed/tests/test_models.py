
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.db.models.deletion import ProtectedError
from django.utils import timezone

from feed.models import Atividade, Equipamento, InstanciaEquipamento, Status, Setor


class DontKnowTheFrameworkTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        admin_group = Group.objects.create(name='administrador')
        health_group = Group.objects.create(name='profissional de saude')

    def setUp(self):
        test_user1 = User.objects.create_user(username="koopa", password="troopa")
        test_user2 = User.objects.create_user(username="peach", password="princess")
        admin_group = Group.objects.get(name='administrador')
        test_user1.groups.set([admin_group])
        test_user2.groups.set([])

        test_user1.save()
        test_user2.save()

        test_equipamento = Equipamento.objects.create(nome="Maquina de ressonancia",
                                                      descricao="Faz MRI e tem campos magneticos")
        test_equipamento2 = Equipamento.objects.create(nome="computador",
                                                       descricao="Auxilia o medico em varias coisas")

        cirurgia = Setor.objects.create(
            nome="cirurgia",
            telefone="+993937747474"
        )

        posmater = Setor.objects.create(
            nome="pos-maternidade",
            telefone="+99123456789"
        )

        for i in range(30):
            equip = test_equipamento if i % 2 else test_equipamento2
            setor = posmater if i % 3 else cirurgia

            InstanciaEquipamento.objects.create(
                equipamento=equip,
                setor=setor,
            )

        inst_equipamento = InstanciaEquipamento.objects.get(pk=10)

        atividade1 = Atividade.objects.create(
            responsavel=test_user1,
            prioridade=4,
            equipamento=inst_equipamento,
        )

        for i in range(10):
            Status.objects.create(
                atividade=atividade1,
                descricao=f'descricao {i}'
            )

    def test_responsavel_nao_administrador(self):
        user = User.objects.get(username__exact="peach")

        atividade2 = Atividade.objects.create(
            responsavel=user,
            prioridade=1,
        )

        atividade2.save()

    def test_responsavel_atividade_set_null(self):
        # Testando models.SET_NULL
        atividade = Atividade.objects.get(pk=1)
        self.assertEqual(atividade.responsavel.username, "koopa")

        responsavel = User.objects.get(username__exact="koopa")
        responsavel.delete()

        atividade = Atividade.objects.get(pk=1)
        self.assertEqual(atividade.responsavel, None)

    def test_delete_all_status_when_deleting_atividade(self):

        delete_random = Status.objects.get(pk=5)
        delete_random.delete()

        atividade = Atividade.objects.get(pk=1)
        # Apenas testando se, ao deletar um status, tambem deletaria a atividade
        print("Testando se atividade ainda esta no banco:", atividade)

        # Testando se todas os estados relacionados a atividade sao deletados junto com a atividade (CASCADE)
        contagem = Status.objects.count()
        self.assertEqual(contagem, 9)

        atividade.delete()
        contagem = Status.objects.count()
        self.assertEqual(contagem, 0)

    def test_protect_instance_when_deleting_equipamento(self):
        instance = InstanciaEquipamento.objects.get(pk=3)
        self.assertEqual(instance.equipamento.nome, "computador")

        computador = Equipamento.objects.get(pk=2)
        self.assertEqual(computador.nome, "computador")

        # Testando delete com models.PROTECT
        with self.assertRaises(ProtectedError):
            computador.delete()

        # Deletando todas as instancias de computador
        instances = InstanciaEquipamento.objects.filter(equipamento__nome__exact="computador")
        instances.delete()

        computador.delete()

        with self.assertRaises(Equipamento.DoesNotExist):
            again = Equipamento.objects.get(pk=2)

    def test_concluir_atividade_seta_tempo_de_finalizacao(self):
        atividade = Atividade.objects.get(pk=1)
        self.assertEqual(atividade.finalizado, None)

        atividade.concluir_atividade()

        new_atividade = Atividade.objects.get(pk=1)
        # Testando se os dados foram salvos corretamente
        self.assertEqual(new_atividade.get_tempo_de_manutencao(), new_atividade.finalizado - new_atividade.inicio)
        self.assertEqual(new_atividade.concluido, True)
