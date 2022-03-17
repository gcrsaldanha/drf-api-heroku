import csv
from datetime import datetime
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from rest_framework.response import Response

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer, SignUpUserSerializer
from agenda.utils import gera_relatorio_prestadores, get_horarios_disponiveis


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
    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)
    if request.query_params.get("formato") == "csv":
        # https://docs.python.org/3/library/csv.html
        # https://docs.djangoproject.com/en/4.0/howto/outputting-csv/#using-the-python-csv-library
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="relatorio_{datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")}.csv"'},
        )
        gera_relatorio_prestadores(response, serializer.data)
        # Acessar essa API pelo navegar: vai iniciar o download
        return response
    else:
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