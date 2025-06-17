from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum
from decimal import Decimal
import datetime

from .forms import (
    RegistroForm, CategoriaForm, TransaccionForm, PresupuestoForm, 
    IngresoForm, FiltroFechaForm
)
from .models import CategoriaGasto, Transaccion, Presupuesto, Ingreso

# Librerías para PDF y Excel (asegúrate de instalarlas: pip install xhtml2pdf openpyxl)
from xhtml2pdf import pisa
from django.template.loader import get_template
import openpyxl
from io import BytesIO


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado correctamente. Ahora inicia sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'gestor/registro.html', {'form': form})


def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'gestor/login.html')


@login_required
def logout_usuario(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    total_gastos = Transaccion.objects.filter(usuario=request.user).aggregate(total=Sum('monto'))['total'] or 0
    total_ingresos = Ingreso.objects.filter(usuario=request.user).aggregate(total=Sum('monto'))['total'] or 0
    balance = total_ingresos - total_gastos
    context = {
        'total_gastos': total_gastos,
        'total_ingresos': total_ingresos,
        'balance': balance,
    }
    return render(request, 'gestor/dashboard.html', context)

@login_required
def grafico_gastos(request):
    categorias = CategoriaGasto.objects.all()
    etiquetas = []
    datos = []
    for categoria in categorias:
        total = Transaccion.objects.filter(
            categoria=categoria,
            usuario=request.user
        ).aggregate(Sum('monto'))['monto__sum'] or 0
        if total > 0:
            etiquetas.append(categoria.nombre)
            datos.append(float(total))
    return render(request, 'gestor/grafico.html', {
        'etiquetas': etiquetas,
        'datos': datos,
    })


@login_required
def alertas_presupuesto(request):
    presupuestos = Presupuesto.objects.filter(usuario=request.user)
    alertas = []
    for presupuesto in presupuestos:
        total_gastado = Transaccion.objects.filter(
            categoria=presupuesto.categoria,
            usuario=request.user
        ).aggregate(Sum('monto'))['monto__sum'] or Decimal('0')

        limite_decimal = Decimal(str(presupuesto.limite))

        if total_gastado >= Decimal('0.8') * limite_decimal:
            porcentaje = round((total_gastado / limite_decimal) * Decimal('100'), 2)
            alertas.append({
                'categoria': presupuesto.categoria.nombre,
                'limite': limite_decimal,
                'gastado': total_gastado,
                'porcentaje': porcentaje,
            })

    return render(request, 'gestor/alertas.html', {
        'alertas': alertas,
    })

