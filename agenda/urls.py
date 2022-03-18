from django.urls import path
<<<<<<< HEAD
from agenda.views import AgendamentoDetail, AgendamentoList, get_horarios, get_relatorio_prestadores, index
=======
from agenda.views import AgendamentoDetail, AgendamentoList, get_horarios, get_relatorio_prestadores, healthcheck
>>>>>>> @{-1}

urlpatterns = [
    path('agendamentos/', AgendamentoList.as_view()),
    path('agendamentos/<int:pk>/', AgendamentoDetail.as_view()),
    path('horarios/', get_horarios),
    path('prestadores/', get_relatorio_prestadores),
    path('', healthcheck),
]
