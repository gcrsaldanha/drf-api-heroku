import json
import requests
from datetime import date
from django.conf import settings


def is_feriado(date: date):
    if settings.TESTING:
        # Se for Natal ou Ano Novo, retornamos True sempre (para testes)
        if (date.day == 25 and date.month == 12) or (date.day == 1 and date.month == 1):
            return True
        return False

    ano = date.year
    r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
    if not r.status_code == 200:
        raise ValueError("Problema ao buscar feriados nacionais")

    feriados = json.loads(r.text)
    for feriado in feriados:
        # datetime.strptime("2020-01-30", "%Y-%m-%d")
        data_as_str = feriado["date"]
        data = date.fromisoformat(data_as_str)  # Formato: "2020-02-20"
        if data == date:
            return True

    return False