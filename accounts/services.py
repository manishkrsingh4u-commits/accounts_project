
from django.db import transaction
from .models import Customer, Account, Transaction
from .serializers import CustomerSerializer, AccountSerializer, TransactionSerializer
from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response
@transaction.atomic
def deposit(account: Account, amount: Decimal, description=None):
    if amount <= 0:
        raise ValueError("Deposit amount must be positive")

    # Lock row to prevent race condition
    account = Account.objects.select_for_update().get(id=account.id)

    account.balance += amount
    account.save(update_fields=['balance'])

    Transaction.objects.create(
        account=account,
        transaction_type="DEPOSIT",
        amount=amount,
        description=description
    )

    return account.balance
@transaction.atomic
def withdraw(account: Account, amount: Decimal, description=None):
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")

    # Lock row
    account = Account.objects.select_for_update().get(id=account.id)

    if account.balance < amount:
        raise ValueError("Insufficient balance")

    account.balance -= amount
    account.save(update_fields=['balance'])

    Transaction.objects.create(
        account=account,
        transaction_type="WITHDRAWAL",
        amount=amount,
        description=description
    )

    return account.balance