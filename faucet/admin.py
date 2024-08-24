from django.contrib import admin

from faucet.models import Transaction

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["wallet_address", "status", "txn_hash", "created_at"]
    search_fields = ("wallet_address", "txn_hash",)
    list_filter = ("wallet_address", "status",)
    ordering = ("-created_at",)