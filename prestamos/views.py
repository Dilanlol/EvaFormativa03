from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render


def es_encargado(user):
    return user.is_authenticated and user.is_staff


@login_required
def inicio(request):
    return render(request, 'prestamos/inicio.html')
