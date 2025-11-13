from rest_framework.throttling import SimpleRateThrottle



class OTPThrottle(SimpleRateThrottle):
    scope = "otp"

    def get_cache_key(self, request, view):
        phone = request.data.get('phone')
        ident = phone or self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
        