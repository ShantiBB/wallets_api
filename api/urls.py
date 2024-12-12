from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.wallet import WalletViewSet

router = DefaultRouter()
router.register('wallets', WalletViewSet, basename='wallet')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
] + router.urls
