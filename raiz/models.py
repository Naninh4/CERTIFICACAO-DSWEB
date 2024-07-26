from django.db import models
from django.utils import timezone

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {'Disponível' if self.disponivel else 'Indisponível'}"


class ItemDeCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"

    def get_preco_total(self):
        return self.produto.preco * self.quantidade


class CarrinhoDeCompra(models.Model):
    data_criacao = models.DateTimeField(default=timezone.now)
    itens = models.ManyToManyField(ItemDeCarrinho, blank=True)

    def __str__(self):
        return f"Carrinho de Compras - {self.data_criacao.strftime('%Y-%m-%d %H:%M:%S')}"

    def get_valor_total(self):
        return sum(item.get_preco_total() for item in self.itens.all())
