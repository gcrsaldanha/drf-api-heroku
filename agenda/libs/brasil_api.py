import json
import requests
from datetime import date


def is_feriado(date: date):
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