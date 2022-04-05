import csv
from io import StringIO

from django.contrib.auth.models import User

from agenda.serializers import PrestadorSerializer
from tamarcado.celery import app
from django.core.mail import EmailMessage


@app.task
def gera_relatorio_prestadores():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "prestador",
            "data_horario",
            "nome_cliente",
            "email_cliente",
            "telefone_cliente",
            "cancelado",
        ]
    )

    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)
    for prestador in serializer.data:
        for agendamento in prestador["agendamentos"]:
            writer.writerow(
                [
                    agendamento["prestador"],
                    agendamento["data_horario"],
                    agendamento["nome_cliente"],
                    agendamento["email_cliente"],
                    agendamento["telefone_cliente"],
                    agendamento["cancelado"],
                ]
            )

    email = EmailMessage(
        "tamarcado - Relatório de prestadores",
        "Em anexo o relatório solicitado.",
        "gabrielcrsaldanha@gmail.com",
        ["gcrsaldanha@gmail.com"],
    )
    email.attach("relatorio.csv", output.getvalue(), "text/csv")
    email.send()
