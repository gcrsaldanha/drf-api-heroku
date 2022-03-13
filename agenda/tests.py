import json
from rest_framework.test import APITestCase
from datetime import datetime, timezone

from agenda.models import Agendamento
from django.contrib.auth.models import User

# Create your tests here.
class TestListagemAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        User.objects.create_user(email="seuze@email.com", username="seuze", password="123")
        self.client.login(username="seuze", password="123")
        response = self.client.get("/api/agendamentos/?username=seuze")
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listagem_de_agendamentos_criados(self):
        seuze = User.objects.create_user(email="seuze@email.com", username="seuze", password="123")
        self.client.login(username="seuze", password="123")
        Agendamento.objects.create(
            data_horario=datetime(2022, 3, 15, tzinfo=timezone.utc),
            nome_cliente="Alice",
            email_cliente="alice@email.com",
            telefone_cliente="99998888",
            prestador=seuze,
        )

        agendamento_serializado = {
            "id": 1,
            "data_horario": "2022-03-15T00:00:00Z",
            "nome_cliente": "Alice",
            "email_cliente": "alice@email.com",
            "telefone_cliente": "99998888",
            "prestador": "seuze",
            "cancelado": False,
        }

        response = self.client.get("/api/agendamentos/?username=seuze")
        data = json.loads(response.content)
        self.assertDictEqual(data[0], agendamento_serializado)


class TestCriacaoAgendamento(APITestCase):
    def test_cria_agendamento(self):
        seuze = User.objects.create_user(email="seuze@email.com", username="seuze", password="123")
        # Não precisa de login!
        # self.client.login(username="seuze", password="123")
        agendamento_request_data = {
            "prestador": "seuze",
            "data_horario": "2022-03-15T00:00:00Z",
            "nome_cliente": "Alice",
            "email_cliente": "alice@email.com",
            "telefone_cliente": "99998888",
        }

        response = self.client.post("/api/agendamentos/", agendamento_request_data)
        self.assertEqual(response.status_code, 201)

        agendamento_criado = Agendamento.objects.get()
        self.assertEqual(agendamento_criado.data_horario, datetime(2022, 3, 15, tzinfo=timezone.utc))
        self.assertEqual(agendamento_criado.prestador, seuze)

    def test_cancela_agendamento(self):
        seuze = User.objects.create_user(email="seuze@email.com", username="seuze", password="123")
        self.client.login(username="seuze", password="123")
        agendamento_request_data = {
            "prestador": "seuze",
            "data_horario": "2022-03-15T00:00:00Z",
            "nome_cliente": "Alice",
            "email_cliente": "alice@email.com",
            "telefone_cliente": "99998888",
        }

        response = self.client.post("/api/agendamentos/", agendamento_request_data)
        self.assertEqual(response.status_code, 201)

        agendamento_criado = Agendamento.objects.get()
        self.assertEqual(agendamento_criado.cancelado, False)

        response = self.client.delete(f"/api/agendamentos/{agendamento_criado.pk}/", agendamento_request_data)
        self.assertEqual(response.status_code, 204)

        agendamento_criado.refresh_from_db()
        self.assertEqual(agendamento_criado.cancelado, True)