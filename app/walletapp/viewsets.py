from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app.walletapp.models import Wallet, Transaction
from app.walletapp.serializers import WalletSerializer, TransactionSerializer


class WalletViewSet(viewsets.ModelViewSet):
    '''viewsets для кошелька'''
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def filter_queryset(self, queryset):
        '''
            Метод возращающий отфилтрованный queryset с кошельками
        '''
        return queryset.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        '''
            Метод добавляющий user_id в Wallet,
            перед сохранением. user_id берем из request
        '''
        serializer.validated_data['user_id'] = self.request.user.id
        serializer.save()

    def get_transaction_list(self, wallet_id):
        '''
            Метод возращающий сериализационный список Transaction
        '''
        transactions = Transaction.objects.filter(wallet_id=wallet_id)
        return TransactionSerializer(transactions, many=True).data

    def perform_destroy(self, instance):
        '''
            Метод проверяющий что баланс не равен 0 перед удалением кошелька
        '''
        if instance.balance != 0:
            raise PermissionDenied
        instance.delete()

    @action(detail=True, methods=['get'])
    def transaction_list(self, request, pk=None):
        '''
            Метод возращающий список операций
        '''
        return Response(self.get_transaction_list(wallet_id=pk))


class TransactionViewSet(viewsets.ModelViewSet):
    '''viewsets для транзакции'''
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
