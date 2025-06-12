from django.contrib import admin
from .models import RegistroGanho

@admin.register(RegistroGanho)
class RegistroGanhoAdmin(admin.ModelAdmin):
    list_display = ('data', 'plataforma', 'corridas', 'valor_bruto', 'promocoes', 'gorjeta', 'valor_liquido')
