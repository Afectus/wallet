from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver, Signal
from django.core.validators import MinValueValidator


class Wallet(models.Model):
    '''ORM Модель кошелька'''
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    balance = models.DecimalField(
        verbose_name='Баланс',
        max_digits=20,
        decimal_places=2,
        default=0
    )
    name = models.CharField(max_length=25, verbose_name='Название кошелька')

    class Meta:
        ordering = ['-id']
        verbose_name = u'Кошелек'
        verbose_name_plural = u'Кошельки'

    def __str__(self):
        return u'%s %s %s' % (self.id, self.name, self.balance)


class Transaction(models.Model):
    '''ORM Модель транзакции'''
    transaction_add = 'add'
    transaction_remove = 'remove'
    choise_transaction_type = (
        (transaction_add, '+'),
        (transaction_remove, '-'),
    )
    wallet = models.ForeignKey(
        to=Wallet,
        on_delete=models.CASCADE,
        verbose_name='Кошелек'
    )
    value = models.DecimalField(
        verbose_name='Сумма',
        max_digits=20,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    transaction_type = models.CharField(
        max_length=10,
        verbose_name='Тип операции',
        choices=choise_transaction_type
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    comment = models.TextField(
        max_length=200,
        verbose_name='Комментарий',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-id']
        verbose_name = u'Операция'
        verbose_name_plural = u'Операции'

    def __str__(self):
        return u'%s %s %s' % (self.id, self.value, self.transaction_type)


@receiver(pre_save, sender=Transaction)
def update_wallet_balance_after_save(sender, instance, **kwargs):
    '''Обновление баланса после сохранения транзакции'''
    walet_object = instance.wallet
    value = 0.0
    if instance.id:
        old_transaction = Transaction.objects.get(id=instance.id)
        value = instance.value - old_transaction.value
        if old_transaction.transaction_type != instance.transaction_type:
            value = instance.value + old_transaction.value
            if instance.value - old_transaction.value == 0:
                value = instance.value
    else:
        value = instance.value

    if instance.transaction_type == Transaction.transaction_add:
        walet_object.balance += value
    if instance.transaction_type == Transaction.transaction_remove:
        walet_object.balance -= value
    walet_object.save()


@receiver(post_delete, sender=Transaction)
def update_wallet_balance_after_delete(sender, instance, **kwargs):
    '''Обновление баланса после удаления транзакции'''
    walet_object = instance.wallet
    if instance.transaction_type == Transaction.transaction_add:
        walet_object.balance -= instance.value
    if instance.transaction_type == Transaction.transaction_remove:
        walet_object.balance += instance.value
    walet_object.save()
