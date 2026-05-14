from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from accounts.views import UsuarioModelViewSet
router = DefaultRouter()
router.register(r'usuarios', UsuarioModelViewSet, basename='usuario')

urlpatterns = [
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/', include(router.urls)),
]