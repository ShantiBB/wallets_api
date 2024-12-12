from rest_framework.routers import DefaultRouter

from api.views.wallet import WalletViewSet

router = DefaultRouter()
router.register('wallets', WalletViewSet, basename='wallet')


urlpatterns = router.urls
