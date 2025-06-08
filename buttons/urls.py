from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.iniciar, name="iniciar"),
    path('inserir/<str:tabela>/', views.formulario, name="formulario"),
    path('editar/<str:tabela>/<int:pk>/', views.formulario, name='editar'),
    path('listar/<str:tabela>/', views.listar, name='listar'),
    path('deletar/<str:tabela>/<int:pk>/', views.deletar, name='deletar'),
    path('cidades-por-estado/<str:estado_id>/', views.cidades_por_estado, name='cidades_por_estado')
]

