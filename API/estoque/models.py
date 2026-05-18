from django.db import models

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-id']

class Produto(models.Model):
    nome = models.CharField(max_length=100)

    preco_compra = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']


class Movimentacao(models.Model):
    autor = models.ForeignKey('accounts.Usuario', on_delete=models.CASCADE, related_name='movimentacoes')
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    tipo_movimentacao = models.CharField(max_length=20,
        choices=[('venda', 'Venda'), ('perda', 'Perda'), ('entrada', 'Entrada')]
    )
    class Meta:
        ordering = ['-id']


class ItemMovimentacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    movimentacao = models.ForeignKey('Movimentacao', on_delete=models.CASCADE, related_name='itens')
    quantidade = models.IntegerField()
    class Meta:
        ordering = ['-id']