from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.iniciar, name="iniciar"),
    path('inserir/<str:tabela>/', views.inserir, name="inserir"),
    path('listar/<str:tabela>/', views.listar, name='listar'),
    re_path(r'^editar/(?P<tabela>\w+)(?:/(\d+)){1,2}/$', views.editar, name='editar'),
    re_path(r'^deletar/(?P<tabela>\w+)(?:/(\d+)){1,2}/$', views.deletar, name='deletar'),
    path('cidades-por-estado/<str:estado_id>/', views.cidades_por_estado, name='cidades_por_estado')
]
