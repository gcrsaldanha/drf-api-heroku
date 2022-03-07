from django.urls import path
from agenda.views import agendamento_detail, agendamento_list, get_horarios

urlpatterns = [
    path('agendamentos/', agendamento_list),
    path('agendamentos/<int:id>/', agendamento_detail),
    path('horarios/', get_horarios),
]
