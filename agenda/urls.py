from django.urls import path
# from agenda.views import agendamento_detail, agendamento_list, get_horarios
from agenda.views import AgendamentoDetail, AgendamentoList, PrestadorList, get_horarios

urlpatterns = [
    path('agendamentos/', AgendamentoList.as_view()),
    path('agendamentos/<int:pk>/', AgendamentoDetail.as_view()),
    path('horarios/', get_horarios),
    path('prestadores/', PrestadorList.as_view()),
]
