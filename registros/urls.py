from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_ganho, name='registrar_ganho'),
    path('editar/<int:pk>/', views.editar_registro, name='editar_registro'),
    path('excluir/<int:pk>/', views.excluir_registro, name='excluir_registro'),

    # Despesas:
    path('despesas/', views.registrar_despesa, name='registrar_despesa'),
    path('despesas/editar/<int:pk>/', views.editar_despesa, name='editar_despesa'),
    path('despesas/excluir/<int:pk>/', views.excluir_despesa, name='excluir_despesa'),
    path('analise/', views.analise_faturamento, name='analise_faturamento'),

    # Login/Logout/Registro
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
]
