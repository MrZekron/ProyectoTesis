from django.urls import path
from App import views  # Importa correctamente el módulo views

urlpatterns = [
    path('registrar-dispositivo/', views.registrar_dispositivo, name='registrar_dispositivo'),
    path('registrar-tanque/', views.registrar_tanque_agua, name='registrar_tanque_agua'),
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registro-usuario/', views.registro_usuario, name='registro_usuario'),
    path('registrar-dispositivo/', views.registrar_dispositivo, name='registrar_dispositivo'),
    path('registrar-tanque/', views.registrar_tanque, name='registrar_tanque'),


    path('menu/', views.menu, name='menu'),



    path('', views.inicio, name='inicio'),  # Vista de inicio
]
