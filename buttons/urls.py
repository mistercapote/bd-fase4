from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.iniciar, name="iniciar"),
    path('inserir/<str:tabela>/', views.inserir, name="inserir"),
    # path('atualizar/<str:tabela>/', views.atualizar, name="atualizar"),
    # path('listar/<str:tabela>/', views.listar, name="listar"),
    # path('deletar/<str:tabela>/', views.deletar, name="deletar")
]

