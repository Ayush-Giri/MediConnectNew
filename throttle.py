from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class ProfileThrottle(UserRateThrottle):
    # now this throttling is tracked based on user
    scope = 'user_profile'



class SignUpThrottle(AnonRateThrottle):
    scope = 'sign_up'