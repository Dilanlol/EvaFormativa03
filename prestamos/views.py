from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CategoriaForm, HerramientaForm
from .models import Categoria, Herramienta, Prestamo


def es_encargado(user):
    return user.is_authenticated and user.is_staff


@login_required
def inicio(request):
    return render(request, 'prestamos/inicio.html')


@login_required
@user_passes_test(es_encargado)
def categoria_list(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'prestamos/categoria_list.html', {'categorias': categorias})


@login_required
@user_passes_test(es_encargado)
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'prestamos/categoria_form.html', {'form': form, 'titulo': 'Nueva categoría'})


@login_required
@user_passes_test(es_encargado)
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'prestamos/categoria_form.html', {'form': form, 'titulo': 'Editar categoría'})


@login_required
@user_passes_test(es_encargado)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        try:
            categoria.delete()
        except ProtectedError:
            messages.error(request, 'No se puede eliminar la categoría porque tiene herramientas asociadas.')
            return redirect('categoria_list')
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('categoria_list')
    return render(request, 'prestamos/categoria_confirm_delete.html', {'categoria': categoria})


@login_required
@user_passes_test(es_encargado)
def herramienta_list(request):
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    herramientas = Herramienta.objects.select_related('categoria').all().order_by('codigo')

    if query:
        herramientas = herramientas.filter(Q(nombre__icontains=query) | Q(codigo__icontains=query))
    if categoria_id:
        herramientas = herramientas.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all().order_by('nombre')
    context = {
        'herramientas': herramientas,
        'categorias': categorias,
        'query': query,
        'categoria_id': categoria_id,
    }
    return render(request, 'prestamos/herramienta_list.html', context)


@login_required
@user_passes_test(es_encargado)
def herramienta_detail(request, pk):
    herramienta = get_object_or_404(Herramienta.objects.select_related('categoria'), pk=pk)
    return render(request, 'prestamos/herramienta_detail.html', {'herramienta': herramienta})


@login_required
@user_passes_test(es_encargado)
def herramienta_create(request):
    if request.method == 'POST':
        form = HerramientaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Herramienta creada correctamente.')
            return redirect('herramienta_list')
    else:
        form = HerramientaForm()
    return render(request, 'prestamos/herramienta_form.html', {'form': form, 'titulo': 'Nueva herramienta'})


@login_required
@user_passes_test(es_encargado)
def herramienta_update(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == 'POST':
        form = HerramientaForm(request.POST, instance=herramienta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Herramienta actualizada correctamente.')
            return redirect('herramienta_list')
    else:
        form = HerramientaForm(instance=herramienta)
    return render(request, 'prestamos/herramienta_form.html', {'form': form, 'titulo': 'Editar herramienta'})


@login_required
@user_passes_test(es_encargado)
def herramienta_delete(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == 'POST':
        try:
            herramienta.delete()
        except ProtectedError:
            messages.error(request, 'No se puede eliminar la herramienta porque tiene préstamos asociados.')
            return redirect('herramienta_list')
        messages.success(request, 'Herramienta eliminada correctamente.')
        return redirect('herramienta_list')
    return render(request, 'prestamos/herramienta_confirm_delete.html', {'herramienta': herramienta})


@login_required
def catalogo(request):
    herramientas = Herramienta.objects.filter(disponible=True).exclude(estado='En reparación').select_related('categoria').order_by('nombre')
    return render(request, 'prestamos/catalogo.html', {'herramientas': herramientas})


@login_required
@require_POST
def agregar_solicitud(request, id):
    herramienta = get_object_or_404(Herramienta, pk=id)
    solicitud = request.session.get('solicitud', [])

    if not herramienta.disponible or herramienta.estado == 'En reparación':
        messages.error(request, 'La herramienta no está disponible para préstamo.')
    elif id in solicitud:
        messages.warning(request, 'La herramienta ya fue agregada a tu solicitud.')
    elif len(solicitud) >= 3:
        messages.error(request, 'Solo puedes solicitar hasta 3 herramientas a la vez.')
    else:
        solicitud.append(id)
        request.session['solicitud'] = solicitud
        request.session.modified = True
        messages.success(request, 'Herramienta agregada a la solicitud.')

    return redirect('catalogo')


@login_required
def ver_solicitud(request):
    ids = request.session.get('solicitud', [])
    herramientas = Herramienta.objects.filter(pk__in=ids).select_related('categoria').order_by('nombre')
    return render(request, 'prestamos/solicitud.html', {'herramientas': herramientas, 'ids': ids})


@login_required
@require_POST
def quitar_solicitud(request, id):
    solicitud = request.session.get('solicitud', [])
    if id in solicitud:
        solicitud.remove(id)
        request.session['solicitud'] = solicitud
        request.session.modified = True
        messages.info(request, 'Herramienta quitada de la solicitud.')
    return redirect('ver_solicitud')


@login_required
@require_POST
@transaction.atomic
def confirmar_solicitud(request):
    ids = request.session.get('solicitud', [])
    if not ids:
        messages.warning(request, 'No hay herramientas en tu solicitud.')
        return redirect('catalogo')

    herramientas = Herramienta.objects.filter(pk__in=ids)
    creados = 0
    for herramienta in herramientas:
        if not herramienta.disponible or herramienta.estado == 'En reparación':
            messages.error(request, f'La herramienta {herramienta.nombre} no está disponible.')
            continue

        Prestamo.objects.create(
            socio=request.user,
            herramienta=herramienta,
            fecha_devolucion_esperada=timezone.localdate() + timedelta(days=7),
            estado='Pendiente',
        )
        herramienta.disponible = False
        herramienta.save(update_fields=['disponible'])
        creados += 1

    request.session.pop('solicitud', None)
    request.session.modified = True

    if creados:
        messages.success(request, f'Se confirmaron {creados} préstamos correctamente.')
    else:
        messages.warning(request, 'No se pudo confirmar ninguna solicitud.')

    return redirect('mis_prestamos')
