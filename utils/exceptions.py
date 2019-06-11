class LoginRequired(Exception):
    "Custom exception for login required"
    pass


class SubscriptionPackageRequired(Exception):
    "Custom exception for Subscription Package Required"
    pass


class NodownloadsLeft(Exception):
    "Custom exception for No downloads left"
    pass


class PremiumUsersOnly(Exception):
    "Custom exception Premium users only"
    pass


class SubscriptionPackageExpired(Exception):
    "Custom exception for SUBSCRIPTION PACKAGE REQUIRED HAS EXPIRED"
    pass
