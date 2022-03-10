from datetime import datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import generics, permissions, authentication

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer
from agenda.utils import get_horarios_disponiveis


class IsOwnerOrCreateOnly(permissions.BasePermission):
    """
    Permissão que verifica se usuário é o "dono" (prestador de serviço) pelo username passado
    ou se é um método para criar agendamento (POST).
    """
    message = "Apenas prestadores podem ver seus agendamentos"

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        if request.user.username and request.user.username == request.query_params.get("username"):
            # Cuidado com o AnonymousUser do Django! user.username = ""
            return True
        # Isso é uma ambiguidade do Django Rest Framework que autenticação também é verificada
        # Precisamos dizer explicitamente que essa view não tem autenticação: authentication_classes = []
        # raise PermissionDenied(detail=self.message)
        return False


class IsOwner(permissions.BasePermission):
    """
    Permissão que verifica se o usuário é o prestador do objeto específico (Agendamento.prestador)
    """
    message = "Apenas o prestador de serviço do objeto pode editar um agendamento"

    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True
        return False
    

class AgendamentoList(generics.ListCreateAPIView):  # /api/agendamentos/
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]
    authentication_classes = []  # Para evitar erros de autenticação e exibir a mensagem de erro da permissão
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        return Agendamento.objects.filter(prestador__username=username)  # Se não for passado username, não retorna nada.


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):  # /api/agendamentos/<pk>/
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwner]
    authentication_classes = [authentication.BasicAuthentication]


@api_view(http_method_names=["GET"])
def get_horarios(request):
    data = request.query_params.get("data")
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
    
    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return JsonResponse(horarios_disponiveis, safe=False)