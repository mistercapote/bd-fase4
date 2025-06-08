from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.iniciar, name="iniciar"),
    path('inserir/<str:tabela>/', views.inserir, name="inserir"),
    path('listar/<str:tabela>/', views.listar, name='listar'),
    path('editar/<str:tabela>/<int:pk>/', views.editar, name='editar'),
    path('deletar/<str:tabela>/<int:pk>/', views.deletar, name='deletar'),
    path('cidades-por-estado/<str:estado_id>/', views.cidades_por_estado, name='cidades_por_estado')
]
