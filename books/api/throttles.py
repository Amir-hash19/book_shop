from rest_framework.throttling import AnonRateThrottle



class SignUpRatethrottle(AnonRateThrottle):
    scope = 'signup'