from asyncio import run

from celery import shared_task
from web3.exceptions import TransactionNotFound, TransactionIndexingInProgress

from faucet.models import Transaction
from faucet.serializer import TxnPendingException
from faucet.utils import failed_fallback
from utils.blockchain import get_txn_receipt
from utils.backoff_func import retry_with_exponential_backoff


@shared_task(name="Check and Update Blockchain txn")
def check_and_update_task(txn_id, txn_hash):
    """
    Check to see if transaction receipt exist in the blockchain
    Updates the `Transaction` db accordingly
    """
    async def async_task():
        '''Refactored to make a bit Non Blokcking :)'''
        @retry_with_exponential_backoff(max_retries=10,
                                jitter=True, 
                                errors=(
                                    TxnPendingException,
                                    TransactionIndexingInProgress, 
                                    TransactionNotFound,
                                    ),
                                fallback_func= failed_fallback)
        def check_and_update_txn():
            print("Checking and updating txns")
            transaction = Transaction.objects.get(id=txn_id)
            tx = get_txn_receipt(txn_hash)#I decided to leave it synchronous
            txn_status, txn_receipt = tx
            print(tx, transaction)
            if tx is None:#this block might never execute of the web3.exceptions raising exceptions on null txns receipts
                raise TxnPendingException
            if tx and txn_status:
                #transaction.update(status=Transaction.TxnStatus.CONFIRMED)
                transaction.mark_as_confirmed(txn_receipt.get("blockNumber"))
            if tx and  not txn_status:
                #transaction.update(status=Transaction.TxnStatus.FAILED)
                transaction.mark_as_failed()
            return txn_receipt.status
        return await check_and_update_txn()
    return run(async_task())

