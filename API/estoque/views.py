from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Produto, Categoria, ItemMovimentacao, Movimentacao
from .serializers import ProdutoSerializer, CategoriaSerializer, ItemMovimentacaoSerializer, MovimentacaoSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

class CategoriaViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProdutoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    @action(detail=True, methods=['get'])
    def produtos(self, request, pk=None):
        categoria = self.get_object()
        produtos = Produto.objects.filter(categoria=categoria)
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)

class ItemMovimentacaoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ItemMovimentacao.objects.all()
    serializer_class = ItemMovimentacaoSerializer

class MovimentacaoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer

