from django.db import models
from django.core.validators import MinValueValidator

from utils.model_abstracts import Model

# Create your models here.
class Transaction(Model):
    """
    `faucet.transaction` model schema
    Stores a single transaction entry
    """
    class TxnStatus(models.TextChoices):
        """An implementation of Status choices field using Textchoices class"""
        PENDING = "pending", "PENDING"
        CONFIRMED = "confirmed", "CONFIRMED"
        FAILED = "failed", "FAILED"
    wallet_address = models.CharField(verbose_name="address", max_length=100)
    testnet = models.BooleanField(default=True)
    currency = models.CharField(default="Sepolia ETH", max_length=50)
    txn_hash = models.CharField(null=True, blank=True, max_length=255)#blockchain transaction hash
    block_number = models.CharField(null=True, blank=True, max_length=255)#blockchain transaction blocks hash
    amount = models.DecimalField(default=0.0001, decimal_places=4, max_digits=5, validators=[MinValueValidator(0.0001)])
    status = models.CharField(max_length=50, default=TxnStatus.PENDING, choices=TxnStatus.choices)  # e.g., pending, completed, failed
    blockchain = models.CharField(default="ETHEREUM", max_length=50)  # e.g., Eth, Polygon, Arbitrum etc
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction #{self.pk} - To: {self.wallet_address}, Amount: {self.amount}, Status:{self.status}"
    
    def mark_as_confirmed(self, block_number):
        """
        Method to mark the Transaction as confirmed/completed.
        """
        if self.status != Transaction.TxnStatus.CONFIRMED:
            self.status = Transaction.TxnStatus.CONFIRMED
            self.block_number = block_number
            print("marking as confirmed")
            self.save()
    
    def mark_as_failed(self):
        """
        Method to mark the order as delivered.
        """
        if self.status != Transaction.TxnStatus.FAILED:
            self.status = Transaction.TxnStatus.FAILED
            print("marking as failed")
            self.save()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]
