from rest_framework import serializers
from .models import Produto, Categoria, ItemMovimentacao, Movimentacao
from django.db import transaction

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)

    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True
    )
    quantidade = serializers.IntegerField(min_value=0, default=0)

    class Meta:
        model = Produto
        fields = fields = [
            'id',
            'nome',
            'preco_compra',
            'preco_venda',
            'quantidade',
            'categoria',
            'categoria_id',
        ]

class ItemMovimentacaoSerializer(serializers.ModelSerializer):
    produto = serializers.PrimaryKeyRelatedField(
        queryset=Produto.objects.all()
    )

    class Meta:
        model = ItemMovimentacao
        fields = ['produto', 'quantidade']

class MovimentacaoSerializer(serializers.ModelSerializer):
    itens = ItemMovimentacaoSerializer(many=True, required=True)
    autor_nome = serializers.CharField(source='autor.username', read_only=True)
    class Meta:
        model = Movimentacao
        fields = [
            'id',
            'autor',
            'autor_nome',
            'data_movimentacao',
            'tipo_movimentacao',
            'itens'
        ]
        read_only_fields = ['autor', 'data_movimentacao']
    def validate(self, attrs):
        tipo = attrs.get('tipo_movimentacao')
        itens = attrs.get('itens', [])

        request = self.context.get('request')

        if tipo == 'venda' and not itens:
            raise serializers.ValidationError({
                'itens': 'Movimentação deve conter itens.'
            })

        if (
            tipo != 'venda'
            and request.user.is_authenticated
            and not request.user.is_staff
        ):
            raise serializers.ValidationError({
                'tipo_movimentacao':
                'Apenas administradores podem criar este tipo de movimentação.'
            })

        for item in itens:
            produto = item['produto']
            quantidade = item['quantidade']
            if(quantidade <= 0):
                raise serializers.ValidationError({
                    'quantidade':
                    f'Quantidade do produto {produto.nome} é inválida.'
                })
            if produto.quantidade < quantidade and (tipo == 'venda' or tipo == 'perda'):
                raise serializers.ValidationError({
                    'estoque':
                    f'Produto {produto.nome} não tem estoque suficiente.'
                })

        return attrs
    @transaction.atomic
    def create(self, validated_data):
        itens_data = validated_data.pop('itens')

        movimentacao = Movimentacao.objects.create(
            **validated_data
        )

        for item_data in itens_data:
            produto = item_data['produto']
            quantidade = item_data['quantidade']

            ItemMovimentacao.objects.create(
                movimentacao=movimentacao,
                **item_data
            )

            if movimentacao.tipo_movimentacao == 'venda':
                produto.quantidade -= quantidade

            elif movimentacao.tipo_movimentacao == 'entrada':
                produto.quantidade += quantidade

            produto.save()

        return movimentacao