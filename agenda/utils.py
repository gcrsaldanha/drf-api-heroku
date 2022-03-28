import csv
from typing import Iterable
from datetime import date, datetime, timedelta, timezone
from agenda.libs import brasil_api

from agenda.models import Agendamento


def get_horarios_disponiveis(data: date) -> Iterable[datetime]:
    # TODO: como melhorar a performance desse programa? Análise de complexidade?
    """
    Retorna uma lista com objetos do tipo datetime cujas datas são o mesmo dia passado (data)
    e os horários são os horários disponíveis para aquele dia, conforme outros agendamentos existam.
    """
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


def gera_relatorio_prestadores(output, prestadores_data):
    writer = csv.writer(output)
    writer.writerow([
        "prestador",
        "data_horario",
        "nome_cliente",
        "email_cliente",
        "telefone_cliente",
        "cancelado",
    ])
    for prestador in prestadores_data:
        for agendamento in prestador["agendamentos"]:
            writer.writerow([
                agendamento["prestador"],
                agendamento["data_horario"],
                agendamento["nome_cliente"],
                agendamento["email_cliente"],
                agendamento["telefone_cliente"],
                agendamento["cancelado"],
            ])