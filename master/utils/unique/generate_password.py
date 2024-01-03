import string
import random

def generate_unique_password(digits=8):
    """
    This function will generate unique password with given digits.
    
    By default will generate 8 digit password.
    """
    symbols = '_@$-' + string.ascii_letters + string.digits
    password = ''
    for digit in range(1, digits+1):
        password += symbols[random.randint(1, len(symbols)-1)]
    return password.upper()