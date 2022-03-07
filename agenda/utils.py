from typing import Iterable
from datetime import date, datetime, timedelta, timezone

from agenda.models import Agendamento


def get_horarios_disponiveis(data: date) -> Iterable[datetime]:
    """
    Retorna uma lista com objetos do tipo datetime cujas datas são o mesmo dia passado (data)
    e os horários são os horários disponíveis para aquele dia, conforme outros agendamentos existam.
    """
    start = datetime(year=data.year, month=data.month, day=data.day, hour=9, minute=0, tzinfo=timezone.utc)
    end = datetime(year=data.year, month=data.month, day=data.day, hour=18, minute=0, tzinfo=timezone.utc)
    delta = timedelta(minutes=30)
    horarios_disponiveis = set()
    while start < end:
        if not Agendamento.objects.filter(data_horario=start).exists():
            horarios_disponiveis.add(start)
        start = start + delta

    return horarios_disponiveis


# TODO: como melhorar a performance desse programa?
# TODO: e se não pudéssemos garantir que o agendamento foi realizado no horário certinho? Ou seja, poderíamos ter um agendamento para 09:15 que ocuparia os horários de 09:00 e 09:30.
# TODO: e se tivéssemos agendamentos com horários variados?