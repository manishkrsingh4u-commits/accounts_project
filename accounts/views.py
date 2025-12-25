from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal

from .models import Account
from .services import deposit
from .services import withdraw
from accounts.models import Customer, Account, Transaction
from accounts.serializers import CustomerSerializer, AccountSerializer, TransactionSerializer

# Create your views here.


class DepositAPIView(APIView):
    def post(self, request):
        try:
            account_id = request.data.get("account_id")
            amount = request.data.get("amount")
            description = request.data.get("description", "")

            if not account_id or not amount:
                return Response(
                    {"error": "account_id and amount are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            account = Account.objects.get(id=account_id)

            new_balance = deposit(
                account=account,
                amount=Decimal(amount),
                description=description
            )

            return Response(
                {
                    "message": "Deposit successful",
                    "account_id": account.id,
                    "balance": new_balance
                },
                status=status.HTTP_200_OK
            )

        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class WithdrawAPIView(APIView):
    def post(self, request):
        try:
            account_id = request.data.get("account_id")
            amount = request.data.get("amount")
            description = request.data.get("description", "")

            if not account_id or not amount:
                return Response(
                    {"error": "account_id and amount are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            account = Account.objects.get(id=account_id)

            new_balance = withdraw(
                account=account,
                amount=Decimal(amount),
                description=description
            )

            return Response(
                {
                    "message": "Withdrawal successful",
                    "account_id": account.id,
                    "balance": new_balance
                },
                status=status.HTTP_200_OK
            )

        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class CustomerApiView(APIView):
    def get(self,request):
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
class AccountApiView(APIView):
    def get(self,request):
        account = Account.objects.all()
        serializer = AccountSerializer(account,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = AccountSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
    
class AccountDetailsView(APIView):
    def get(self,request,pk):
        try:
            account = Account.objects.get(pk=pk)
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    def put(self,request,pk):
        try:
            account = Account.objects.get(pk=pk)
            serializer = AccountSerializer(account,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )