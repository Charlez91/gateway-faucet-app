from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.fields import (CharField)

from utils.blockchain import check_address, get_account, web3

class TxnPendingException(APIException):
    """
    Exception Raised when `Transaction` is still pending on blockchain
    and yet to be mined. made to help backoff function retry
    """
    status_code = HTTP_400_BAD_REQUEST
    default_detail: str = "Txn is pending"
    default_code: str = "invalid"

class FundSerializer(Serializer):
    wallet_address = CharField(required=True, min_length=40, max_length=42)

    def validate_wallet_address(self, value):
        '''
        validates `wallet_address` field
        Checks whether its an eth address and can accept token
        '''
        if not check_address(str(value)):
            raise ValidationError("Wallet Address Must be A valid ETH address. ENS not supported for now")
        return value
    
