from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_object_or_404, render
from .forms import RegistroGanhoForm, DespesaForm
from .models import Despesa, RegistroGanho
from django.db.models.functions import TruncDate
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

def registrar_ganho(request):
    if request.method == 'POST':
        form = RegistroGanhoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_ganho')
    else:
        form = RegistroGanhoForm()

    registros = RegistroGanho.objects.order_by('-data')

    return render(request, 'registros/formulario.html', {
        'form': form,
        'registros': registros
    })

def excluir_registro(request, pk):
    registro = get_object_or_404(RegistroGanho, pk=pk)
    registro.delete()
    return redirect('registrar_ganho')

def editar_registro(request, pk):
    registro = get_object_or_404(RegistroGanho, pk=pk)
    if request.method == 'POST':
        form = RegistroGanhoForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('registrar_ganho')
    else:
        form = RegistroGanhoForm(instance=registro)
    registros = RegistroGanho.objects.order_by('-data')
    return render(request, 'registros/formulario.html', {'form': form, 'registros': registros})

def registrar_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_despesa')
    else:
        form = DespesaForm()

    despesas = Despesa.objects.order_by('-data')

    return render(request, 'registros/despesas.html', {
        'form': form,
        'despesas': despesas,
    })

def editar_despesa(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk)
    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            return redirect('registrar_despesa')
    else:
        form = DespesaForm(instance=despesa)

    despesas = Despesa.objects.order_by('-data')
    return render(request, 'registros/despesas.html', {
        'form': form,
        'despesas': despesas,
        'editando': True,
        'despesa_id': pk
    })

def excluir_despesa(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk)
    despesa.delete()
    return redirect('registrar_despesa')

def analise_faturamento(request):
    # Cria a expressão da soma: valor_bruto + promocoes + gorjeta
    valor_liquido_expr = ExpressionWrapper(
        F('valor_bruto') + F('promocoes') + F('gorjeta'),
        output_field=DecimalField()
    )

    dados = (
        RegistroGanho.objects
        .values('data')
        .annotate(total=Sum(valor_liquido_expr))
        .order_by('data')
    )

    labels = [item['data'].strftime('%d/%m/%Y') for item in dados]
    valores = [float(item['total']) for item in dados]

    # Soma total do faturamento líquido bruto
    faturamento_bruto = RegistroGanho.objects.aggregate(
        total_bruto=Sum(valor_liquido_expr)
    )['total_bruto'] or 0

    # Soma total das despesas
    total_despesas = Despesa.objects.aggregate(
        total=Sum('valor')
    )['total'] or 0

    # Faturamento líquido = bruto - despesas
    faturamento_liquido = faturamento_bruto - total_despesas

    # Quantidade de dias únicos com ganhos registrados (para média diária)
    dias_unicos = RegistroGanho.objects.values('data').distinct().count()
    media_diaria = faturamento_bruto / dias_unicos if dias_unicos else 0

    return render(request, 'registros/analise.html', {
        'labels': labels,
        'valores': valores,
        'faturamento_bruto': faturamento_bruto,
        'total_despesas': total_despesas,
        'faturamento_liquido': faturamento_liquido,
        'media_diaria': media_diaria,
    })