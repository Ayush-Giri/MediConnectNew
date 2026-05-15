import secrets
import string

def generate_mc_otp():
    digits = ''.join(secrets.choice(string.digits) for _ in range(6))
    return f"MC-{digits}"