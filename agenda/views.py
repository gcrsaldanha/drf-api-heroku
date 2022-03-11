from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import generics, permissions

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from agenda.utils import get_horarios_disponiveis


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
        return Agendamento.objects.filter(prestador__username=username)  # Se não for passado username, não retorna nada.


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):  # /api/agendamentos/<pk>/
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwner]


class PrestadorList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = PrestadorSerializer


@api_view(http_method_names=["GET"])
def get_horarios(request):
    data = request.query_params.get("data")
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
    
    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return JsonResponse(horarios_disponiveis, safe=False)