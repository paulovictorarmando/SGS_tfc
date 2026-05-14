from rest_framework import serializers
from .models import Produto, Categoria, ItemMovimentacao, Movimentacao

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Produto
        fields = '__all__'

class ItemMovimentacaoSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)

    class Meta:
        model = ItemMovimentacao
        fields = '__all__'

class MovimentacaoSerializer(serializers.ModelSerializer):
    itens = ItemMovimentacaoSerializer(read_only=True, many=True)
    tipo_movimentacao = serializers.CharField(source='get_tipo_movimentacao_display')
    class Meta:
        model = Movimentacao
        fields = '__all__'
    def validate_tipo_movimentacao(self, value):
        if value not in ['venda', 'perda', 'entrada', 'ajuste']:
            raise serializers.ValidationError("Tipo de movimentação inválido.")
        if value == 'venda'and not self.initial_data.get('itens'):
            raise serializers.ValidationError("Movimentação deve conter itens.")
        if value != 'venda' and self.context.get('request').user.is_authenticated and not self.context.get('request').user.is_staff:
            raise serializers.ValidationError("Apenas administradores podem criar movimentações de perda, entrada ou ajuste.")
        for item in self.initial_data.get('itens', []):
            produto_id = item.get('produto')
            quantidade = item.get('quantidade')
            try:
                produto = Produto.objects.get(id=produto_id)
                if produto.quantidade < quantidade:
                    raise serializers.ValidationError(f"Produto {produto.nome} não tem estoque suficiente.")
            except Produto.DoesNotExist:
                raise serializers.ValidationError(f"Produto com id {produto_id} não existe.")
        return value