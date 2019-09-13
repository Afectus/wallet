from django.contrib import admin
from app.walletapp.models import Wallet, Transaction

admin.site.register(Wallet)
admin.site.register(Transaction)
