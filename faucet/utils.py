from faucet.models import Transaction

def failed_fallback(*args, **kwargs):
    """
    Fall back function for the backoff retry function
    """
    transaction = Transaction.objects.get(id=args[0])
    transaction.mark_as_failed()

    return "Transaction Failed"