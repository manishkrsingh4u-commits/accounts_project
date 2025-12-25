
from rest_framework import serializers
from django.contrib.auth.models import User 

from .models import Customer, Account, Transaction
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'email', 'phone_number', 'address', 'created_at', 'updated_at']
class AccountSerializer(serializers.ModelSerializer):

    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',       # ⭐ THIS LINE FIXES EVERYTHING
        write_only=True
    )
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'customer','customer_id', 'account_type', 'balance', 'created_at', 'updated_at']
class TransactionSerializer(serializers.ModelSerializer):
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        source='account',       # ⭐ THIS LINE FIXES EVERYTHING
        write_only=True
    )

    account = AccountSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'account','account_id', 'transaction_type', 'amount', 'timestamp', 'description']
