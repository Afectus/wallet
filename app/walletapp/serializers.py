from rest_framework import serializers
from app.walletapp.models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Wallet"""
    balance = serializers.ReadOnlyField()

    class Meta:
        model = Wallet
        fields = (
            'id',
            'balance',
            'name',
        )


class TransactionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Transaction"""

    class Meta:
        model = Transaction
        fields = (
            'id',
            'wallet',
            'value',
            'transaction_type',
            'created_date',
            'comment',
        )
