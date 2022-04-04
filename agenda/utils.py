import csv
from typing import Iterable
from datetime import date, datetime, timedelta, timezone
from agenda.libs import brasil_api

from agenda.models import Agendamento


def get_horarios_disponiveis(data: date) -> Iterable[datetime]:
    """
    Verifica os horários disponíveis para uma determinada data.

    Caso a data passada seja um feriado, nenhum horário disponível é retornado. Para essa consulta
    é utilizada a API de feriados através da função `brasil_api`
    """
    # TODO: como melhorar a performance desse programa? Análise de complexidade?
    if brasil_api.is_feriado(data):
        return []

    start = datetime(year=data.year, month=data.month, day=data.day, hour=9, minute=0, tzinfo=timezone.utc)
    end = datetime(year=data.year, month=data.month, day=data.day, hour=18, minute=0, tzinfo=timezone.utc)
    delta = timedelta(minutes=30)
    horarios_disponiveis = set()
    while start < end:
        if not Agendamento.objects.filter(data_horario=start).exists():
            horarios_disponiveis.add(start)
        start = start + delta

    return horarios_disponiveis
