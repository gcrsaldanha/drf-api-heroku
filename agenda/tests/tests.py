import json
from unittest import mock
from rest_framework.test import APITestCase
from datetime import datetime, time, timezone

from agenda.models import Agendamento
from django.contrib.auth.models import User

class AgendamentoAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.seuze = User.objects.create_user(email="seuze@email.com", username="seuze", password="123")
        self.client.login(username="seuze", password="123")

        return super().setUp()

# Create your tests here.
class TestListagemAgendamentos(AgendamentoAPITestCase):
    def test_listagem_vazia(self):
        response = self.client.get("/api/agendamentos/?username=seuze")
        data = json.loads(response.content)
        assert data == []

    def test_listagem_de_agendamentos_criados(self):
        Agendamento.objects.create(
            data_horario=datetime(2023, 3, 15, 9, tzinfo=timezone.utc),
            nome_cliente="Alice",
            email_cliente="alice@email.com",
            telefone_cliente="99998888",
            prestador=self.seuze,
        )

        agendamento_serializado = {
            "id": 1,
            "data_horario": "2023-03-15T09:00:00Z",
            "nome_cliente": "Alice",
            "email_cliente": "alice@email.com",
            "telefone_cliente": "99998888",
            "prestador": "seuze",
            "cancelado": False,
        }

        response = self.client.get("/api/agendamentos/?username=seuze")
        data = json.loads(response.content)
        assert data[0] == agendamento_serializado


class TestCriacaoAgendamento(AgendamentoAPITestCase):
    def test_cria_agendamento(self):
        agendamento_request_data = {
            "prestador": "seuze",
            "data_horario": "2023-03-15T09:00:00Z",
            "nome_cliente": "Alice",
            "email_cliente": "alice@email.com",
            "telefone_cliente": "99998888",
        }

        response = self.client.post("/api/agendamentos/", agendamento_request_data)
        assert response.status_code == 201

        agendamento_criado = Agendamento.objects.get()
        assert agendamento_criado.data_horario ==  datetime(2023, 3, 15, 9, tzinfo=timezone.utc)
        assert agendamento_criado.prestador == self.seuze
    
    def test_cria_agendamento_no_passado_retorna_400(self):
        agendamento_request_data = {
            "prestador": "seuze",
            "data_horario": "2020-03-15T09:00:00Z",
            "nome_cliente": "Alice",
            "email_cliente": "alice@email.com",
            "telefone_cliente": "99998888",
        }

        response = self.client.post("/api/agendamentos/", agendamento_request_data)
        assert response.status_code == 400

    def test_cancela_agendamento(self):
        agendamento_request_data = {
            "prestador": "seuze",
            "data_horario": "2023-03-15T09:00:00Z",
            "nome_cliente": "Alice",
            "email_cliente": "alice@email.com",
            "telefone_cliente": "99998888",
        }

        response = self.client.post("/api/agendamentos/", agendamento_request_data)
        assert response.status_code == 201

        agendamento_criado = Agendamento.objects.get()
        assert agendamento_criado.cancelado == False

        response = self.client.delete(f"/api/agendamentos/{agendamento_criado.pk}/", agendamento_request_data)
        assert response.status_code == 204

        agendamento_criado.refresh_from_db()
        assert agendamento_criado.cancelado == True


class TestGetHorarios(AgendamentoAPITestCase):
    @mock.patch("agenda.libs.brasil_api.is_feriado", autospec=True, return_value=True)
    # @mock.patch("agenda.utils.brasil_api")
    def test_horarios_disponiveis_feriado_retorna_lista_vazia(self, api_mock):
        # api_mock.is_feriado.return_value = True
        response = self.client.get("/api/horarios/?data=2022-01-01")
        assert response.status_code, 200
        assert response.data == []

    @mock.patch("agenda.libs.brasil_api.is_feriado", autospec=True, return_value=False)
    # @mock.patch("agenda.utils.brasil_api")
    def test_horarios_disponiveis_em_dia_comum_retorna_todos_horarios(self, api_mock):
        # api_mock.is_feriado.return_value = False
        response = self.client.get("/api/horarios/?data=2022-01-02")
        assert response.status_code, 200
        assert not len(response.data) == 0, "Lista vazia!"  # Pra evitar dar out of index error na linha abaixo
        assert response.data[0] == datetime(2022, 1, 2, 9, 0, 0, tzinfo=timezone.utc)
        assert response.data[-1] == datetime(2022, 1, 2, 17, 30, 0, tzinfo=timezone.utc)