
from rest_framework import serializers
from django.contrib.auth.models import User 

from .models import Customer, Account, Transaction
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'email', 'phone_number', 'address', 'created_at', 'updated_at']
class AccountSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'customer', 'account_type', 'balance', 'created_at', 'updated_at']
class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'timestamp', 'description']
