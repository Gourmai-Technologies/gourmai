import random
import string

def generate_payment_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))