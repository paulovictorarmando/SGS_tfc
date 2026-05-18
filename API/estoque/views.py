from urllib import request

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Produto, Categoria, Movimentacao
from .serializers import ProdutoSerializer, CategoriaSerializer, MovimentacaoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class CategoriaViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(
                'Apenas administradores podem criar categorias.'
            )

        return super().create(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(
                'Apenas administradores podem atualizar categorias.'
            )

        return super().update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(
                'Apenas administradores podem deletar categorias.'
            )
        return super().destroy(request, *args, **kwargs)

class ProdutoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(
                'Apenas administradores podem criar produtos.'
            )

        return super().create(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(
                'Apenas administradores podem atualizar produtos.'
            )

        return super().update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(
                'Apenas administradores podem deletar produtos.'
            )
        return super().destroy(request, *args, **kwargs)


class MovimentacaoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MovimentacaoSerializer

    def get_queryset(self):
        user = self.request.user

        #if user.is_staff:
        return Movimentacao.objects.all()

        #return Movimentacao.objects.filter(autor=user)

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

