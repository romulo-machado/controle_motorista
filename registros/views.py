from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegistroGanhoForm, DespesaForm
from .models import Despesa, RegistroGanho
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Decorador para exigir login em todas as views
@login_required
def registrar_ganho(request):
    if request.method == 'POST':
        form = RegistroGanhoForm(request.POST)
        if form.is_valid():
            ganho = form.save(commit=False)
            ganho.user = request.user
            ganho.save()
            return redirect('registrar_ganho')
    else:
        form = RegistroGanhoForm()

    registros = RegistroGanho.objects.filter(user=request.user).order_by('-data')

    return render(request, 'registros/formulario.html', {
        'form': form,
        'registros': registros
    })

@login_required
def excluir_registro(request, pk):
    registro = get_object_or_404(RegistroGanho, pk=pk, user=request.user)
    registro.delete()
    return redirect('registrar_ganho')

@login_required
def editar_registro(request, pk):
    registro = get_object_or_404(RegistroGanho, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RegistroGanhoForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('registrar_ganho')
    else:
        form = RegistroGanhoForm(instance=registro)
    
    registros = RegistroGanho.objects.filter(user=request.user).order_by('-data')
    return render(request, 'registros/formulario.html', {
        'form': form,
        'registros': registros,
        'editando': True,
        'registro_id': pk
    })

@login_required
def registrar_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.user = request.user
            despesa.save()
            return redirect('registrar_despesa')
    else:
        form = DespesaForm()

    despesas = Despesa.objects.filter(user=request.user).order_by('-data')

    return render(request, 'registros/despesas.html', {
        'form': form,
        'despesas': despesas,
    })

@login_required
def editar_despesa(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            return redirect('registrar_despesa')
    else:
        form = DespesaForm(instance=despesa)

    despesas = Despesa.objects.filter(user=request.user).order_by('-data')
    return render(request, 'registros/despesas.html', {
        'form': form,
        'despesas': despesas,
        'editando': True,
        'despesa_id': pk
    })

@login_required
def excluir_despesa(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk, user=request.user)
    despesa.delete()
    return redirect('registrar_despesa')

@login_required
def analise_faturamento(request):
    # Calcula valor líquido: valor_bruto + promoções + gorjeta
    valor_liquido_expr = ExpressionWrapper(
        F('valor_bruto') + F('promocoes') + F('gorjeta'),
        output_field=DecimalField()
    )

    # Dados por dia
    dados = (
        RegistroGanho.objects.filter(user=request.user)
        .values('data')
        .annotate(total=Sum(valor_liquido_expr))
        .order_by('data')
    )

    labels = [item['data'].strftime('%d/%m/%Y') for item in dados]
    valores = [float(item['total']) for item in dados]

    # Totais gerais
    faturamento_bruto = RegistroGanho.objects.filter(user=request.user).aggregate(
        total_bruto=Sum(valor_liquido_expr)
    )['total_bruto'] or 0

    total_despesas = Despesa.objects.filter(user=request.user).aggregate(
        total=Sum('valor')
    )['total'] or 0

    faturamento_liquido = faturamento_bruto - total_despesas

    dias_unicos = RegistroGanho.objects.filter(user=request.user).values('data').distinct().count()
    media_diaria = faturamento_bruto / dias_unicos if dias_unicos else 0

    return render(request, 'registros/analise.html', {
        'labels': labels,
        'valores': valores,
        'faturamento_bruto': faturamento_bruto,
        'total_despesas': total_despesas,
        'faturamento_liquido': faturamento_liquido,
        'media_diaria': media_diaria,
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('registrar_ganho')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('registrar_ganho')
        else:
            return render(request, 'registros/login.html', {'erro': 'Usuário ou senha inválidos'})
    return render(request, 'registros/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('registrar_ganho')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'registros/registro.html', {'erro': 'As senhas não coincidem.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'registros/registro.html', {'erro': 'Usuário já existe.'})
        
        if not username or not email or not password1 or not password2:
            return render(request, 'registros/registro.html', {'erro': 'Todos os campos são obrigatórios.'})


        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('registrar_ganho')

    return render(request, 'registros/registro.html')