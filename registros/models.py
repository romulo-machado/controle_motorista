from django.db import models

class RegistroGanho(models.Model):
    data = models.DateField()
    plataforma = models.CharField(max_length=100)
    corridas = models.PositiveIntegerField()
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    promocoes = models.DecimalField(max_digits=10, decimal_places=2)
    gorjeta = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def valor_liquido(self):
        return self.valor_bruto + self.promocoes + self.gorjeta

    def __str__(self):
        return f"{self.data} - {self.plataforma}"

class Despesa(models.Model):
    data = models.DateField()
    tipo = models.CharField(max_length=50)
    descricao = models.TextField(blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.data} - {self.tipo} - R$ {self.valor}"