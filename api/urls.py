from django.urls import path
from api.views.saude import health_check
from api.views.predicao import PredicaoView
from api.views.informacoes import ModeloInfoView, LimitacoesView

urlpatterns = [
    path('health', health_check, name='health'),
    path('predicao', PredicaoView.as_view(), name='predicao'),
    path('modelo/info', ModeloInfoView.as_view(), name='modelo-info'),
    path('limitacoes', LimitacoesView.as_view(), name='limitacoes'),
]