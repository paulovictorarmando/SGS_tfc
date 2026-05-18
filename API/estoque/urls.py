from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProdutoViewSet, MovimentacaoViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'produtos', ProdutoViewSet, basename='produtos')
router.register(r'movimentacoes', MovimentacaoViewSet, basename='movimentacoes')

urlpatterns = [
    path('api/', include(router.urls)),
]