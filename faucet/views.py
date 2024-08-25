from datetime import datetime, timedelta
from collections import defaultdict

from django.db.models import Count
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from faucet.serializer import FundSerializer, StatsSerializer
from faucet.models import Transaction
from faucet.tasks import check_and_update_task
from utils.throttle import (
                UserBurstRateThrottle, 
                WalletRateThrottle
                )
from utils.blockchain import (
                get_account,
                build_transaction, 
                sign_and_send_txn, 
                get_txn, 
                web3
                )


# Create your views here.
class FundAddressAPIView(APIView):
    """
    The `faucet/fund/` routes View class
    To fund a wallet adddress with 0.0001 Sepolia Eth
    """
    serializer_class= FundSerializer
    throttle_classes = [UserBurstRateThrottle, WalletRateThrottle]
    parser_classes = [JSONParser, FormParser, ]

    @extend_schema(
        summary='Fund Wallet Address View',
        description="This is POST method api endpoint to fund an address with 0.0001 sepolia Eth",
        request= FundSerializer,
        responses={
            200: OpenApiResponse(description='Json Response'),
            400: OpenApiResponse(description='Validation error')
        }
    )

    def get_serializer_context(self):
        return {
            'request':self.request,
            'format': self.format_kwarg,
            'view':self
            }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            wallet_address= serializer.validated_data.get("wallet_address")
            try:
                account = get_account()
                if web3.eth.get_balance(account.address) <= web3.to_wei(0.0001, 'ether'):
                    return Response("Faucet Funds are low. Try Again later", HTTP_400_BAD_REQUEST)
                print("in try block")
                txn_hash = sign_and_send_txn(build_transaction(wallet_address, account=account))
            except(Exception) as e:
                print(e)
            else:
                tx = get_txn(txn_hash)
                print(dir(txn_hash))
                txn_hash_str = txn_hash.hex()
                if tx:
                    transaction = Transaction.objects.create(wallet_address=wallet_address, txn_hash=txn_hash_str)
                    check_and_update_task.delay(transaction.id, txn_hash)
                    return Response({
                        "faucet_txnID":f"{transaction.id}",
                        "transaction_hash":f"{txn_hash_str}",
                        "message":f'''Transfer of 0.0001 Sepolia Eth has been initiated to {wallet_address}.
You can view and track your transaction at https://sepolia.etherscan.io/tx/{txn_hash_str}'''
                        }, HTTP_201_CREATED)
            
            return Response("An Error Occured. Please Try Again later", HTTP_503_SERVICE_UNAVAILABLE)
        else:#if raise exception is set to true this block doesnt execute though
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class TransactionStatsAPIView(APIView):
    """
    The `faucet/stats/` View class implementation
    To get stats of  transactions in the last 24hrs
    """
    serializer_class= StatsSerializer

    @extend_schema(
        summary='Get Transactions Stats View',
        description="This is GET method api endpoint get transaction statistics in the last 24hrs",
        request= StatsSerializer,
        responses={
            200: OpenApiResponse(description='Json Response'),
            400: OpenApiResponse(description='Validation error')
        }
    )

    def get_serializer_context(self):
        return {
            'request':self.request,
            'format': self.format_kwarg,
            'view':self
            }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    
    
    def get(self, request):
        txns = Transaction.objects.\
            filter(created_at__gte = timezone.now() - timedelta(hours=24,)).\
            values("status").annotate(count= Count("id"))
        print(txns)
        res = defaultdict(int)
        for txn in txns:
            if txn.get("status") == "confirmed":
                res["successful_txns"] = txn.get("count")
            if txn.get("status") == "failed":
                res["failed_txns"] = txn.get("count")
        return Response(
            {"successful_txns":res["successful_txns"], 
             "failed_txns":res["failed_txns"], 
             "message":"Transaction stats in the last 24hrs"
            }, 
             HTTP_200_OK)