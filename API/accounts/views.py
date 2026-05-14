from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from accounts.models import Usuario
from accounts.serializers import UsuarioSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

class UsuarioModelViewSet(ModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Usuario.objects.all()


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)