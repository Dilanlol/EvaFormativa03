from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nueva/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),
    path('herramientas/', views.herramienta_list, name='herramienta_list'),
    path('herramientas/nueva/', views.herramienta_create, name='herramienta_create'),
    path('herramientas/<int:pk>/', views.herramienta_detail, name='herramienta_detail'),
    path('herramientas/<int:pk>/editar/', views.herramienta_update, name='herramienta_update'),
    path('herramientas/<int:pk>/eliminar/', views.herramienta_delete, name='herramienta_delete'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('solicitud/agregar/<int:id>/', views.agregar_solicitud, name='agregar_solicitud'),
    path('solicitud/', views.ver_solicitud, name='ver_solicitud'),
    path('solicitud/quitar/<int:id>/', views.quitar_solicitud, name='quitar_solicitud'),
    path('solicitud/confirmar/', views.confirmar_solicitud, name='confirmar_solicitud'),
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('mis-prestamos/cancelar/<int:id>/', views.cancelar_prestamo, name='cancelar_prestamo'),
    path('gestion-prestamos/', views.todos_prestamos, name='todos_prestamos'),
    path('gestion-prestamos/activar/<int:id>/', views.activar_prestamo, name='activar_prestamo'),
    path('gestion-prestamos/devolver/<int:id>/', views.devolver_prestamo, name='devolver_prestamo'),
]
