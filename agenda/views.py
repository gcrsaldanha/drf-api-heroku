import csv
from datetime import datetime
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from rest_framework.response import Response

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer, SignUpUserSerializer
from agenda.utils import get_horarios_disponiveis
from agenda.tasks import gera_relatorio_prestadores


class IsOwnerOrCreateOnly(permissions.BasePermission):
    """
    Permissão que verifica se usuário é o "dono" (prestador de serviço) pelo username passado
    ou se é um método para criar agendamento (POST).
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        if request.user.username == request.query_params.get("username"):
            return True
        return False


class IsOwner(permissions.BasePermission):
    """
    Permissão que verifica se o usuário é o prestador do objeto específico (Agendamento.prestador)
    """

    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True
        return False
    

class AgendamentoList(generics.ListCreateAPIView):  # /api/agendamentos/
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        return Agendamento.objects.filter(prestador__username=username, cancelado=False)  # Se não for passado username, não retorna nada.


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):  # /api/agendamentos/<pk>/
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwner]

    def perform_destroy(self, instance):
        instance.cancelado = True
        instance.save()

@api_view(http_method_names=["GET"])
@permission_classes([permissions.IsAdminUser])
def get_relatorio_prestadores(request):
    if request.query_params.get("formato") == "csv":
        result = gera_relatorio_prestadores.delay()  # AsyncResult(task_id="abc1231")
        return Response({"task_id": result.task_id})
    else:
        prestadores = User.objects.all()
        serializer = PrestadorSerializer(prestadores, many=True)
        return Response(serializer.data)


@api_view(http_method_names=["GET"])
def get_horarios(request):
    data = request.query_params.get("data")
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()

    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return Response(horarios_disponiveis)


@api_view(http_method_names=["GET"])
def healthcheck(request):
    return Response({
        "status": "OK",
        "message": "Deployado!"
    }, status=200)
