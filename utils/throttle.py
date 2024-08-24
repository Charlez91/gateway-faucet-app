from rest_framework.throttling import UserRateThrottle


class UserBurstRateThrottle(UserRateThrottle):
    """
    To limit/throttle request rate per hour
    """
    scope = "burst"


class UserSustainedRateThrottle(UserRateThrottle):
    """
    throttle and limit rate on a per day basis
    """
    scope = "sustained"

class WalletRateThrottle(UserRateThrottle):
    """
    throttle and limit rate on a per day basis
    """
    scope = "burst"

    def get_cache_key(self, request, view):
        if request.data and request.data.get("wallet_address"):
            ident = request.data.get("wallet_address")
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }