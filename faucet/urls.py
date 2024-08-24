from django.urls import path, include
from rest_framework.routers import DefaultRouter

from faucet import views as faucet_views

#specifies appname for name spacing
app_name = "faucet"

urlpatterns = [
    path("faucet/fund/", faucet_views.FundAddressAPIView.as_view(), name="fund"),
    path("faucet/stats/", faucet_views.TransactionStatsAPIView.as_view(), name="stats"),
]
