from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.iniciar, name="iniciar"),
<<<<<<< HEAD
    path('formulario/<str:acao>/<str:tabela>/', views.formulario, name="formulario"),
=======
    path('inserir/<str:tabela>/', views.inserir, name="inserir"),
    # path('atualizar/<str:tabela>/', views.atualizar, name="atualizar"),
>>>>>>> 07864fbb81a40d3ca0d45b09ee04bde2d1503cab
    # path('listar/<str:tabela>/', views.listar, name="listar"),
    # path('deletar/<str:tabela>/', views.deletar, name="deletar")
]

