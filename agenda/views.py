from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer
from agenda.utils import get_horarios_disponiveis


class AgendamentoList(APIView):
    def get(self, request):
        agendamentos = Agendamento.objects.all()
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = request.data
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class AgendamentoDetail(APIView):
    def get(self, request, id):
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializer(obj)
        return JsonResponse(serializer.data)

    def patch(self, request, id):
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return Response(serializer.errors, status=400)
       
    def delete(self, request, id):
        obj = get_object_or_404(Agendamento, id=id)
        obj.delete()
        return Response(status=204)


@api_view(http_method_names=["GET"])
def get_horarios(request):
    data = request.query_params.get("data")
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
    
    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return JsonResponse(horarios_disponiveis, safe=False)