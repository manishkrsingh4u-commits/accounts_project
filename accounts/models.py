from django.db import models

class Customer(models.Model):
    full_name = models.CharField(max_length= 100)
    email = models.CharField(max_length= 100, unique=True)
    phone_number = models.CharField(max_length= 15, unique=True)
    address = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.full_name
       
class Account(models.Model):
    ACCOUNT_TYPES = [
        ('SAVINGS', 'Savings'),
        ('CHECKING', 'Checking'),
        ('BUSINESS', 'Business'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='accounts')
    account_type = models.CharField(max_length= 20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits= 12, decimal_places= 2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.full_name} - {self.account_type} Account"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length= 20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits= 12, decimal_places= 2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length= 255, blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.account}"