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
]
