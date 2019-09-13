from django.urls import path
from rest_framework.routers import DefaultRouter
from app.walletapp.viewsets import WalletViewSet, TransactionViewSet


router = DefaultRouter()
router.register(r'wallet', WalletViewSet, basename='wallet')
router.register(r'transaction', TransactionViewSet, basename='transaction')

urlpatterns = [

] + router.urls
