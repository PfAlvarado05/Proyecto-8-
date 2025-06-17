from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_usuario, name='login'),  # Página principal: login
    path('registro/', views.registro_usuario, name='registro'),
    path('logout/', views.logout_usuario, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('agregar-categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('agregar-transaccion/', views.agregar_transaccion, name='agregar_transaccion'),
    path('agregar-presupuesto/', views.agregar_presupuesto, name='agregar_presupuesto'),
    path('agregar-ingreso/', views.agregar_ingreso, name='agregar_ingreso'),

    path('grafico-gastos/', views.grafico_gastos, name='grafico_gastos'),
    path('alertas-presupuesto/', views.alertas_presupuesto, name='alertas_presupuesto'),

    path('filtro/', views.filtrar_transacciones, name='filtro_transacciones'),

    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
]
