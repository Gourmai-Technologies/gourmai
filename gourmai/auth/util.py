import functools
import os
import hashlib
import binascii
import random
import string
import re

# Flask #
from flask import g

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/

def hash_pass(password):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes

def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""

    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

#IMPORTANT! Called for every request

#WRAPPER FOR COOKIE SETTINGS 
def manage_cookie_policy(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):

        g.showCookieAlert = False #DEFAULT
        if g.policyCode == -1:
            g.showCookieAlert = True

        return view(**kwargs)

    return wrapped_view

def generate_verification_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
def generate_verification_link(verification_token):
    return f"gourmai.co.uk/auth/{verification_token}"

def is_email_valid(email):
    """
    Check if the email format is valid.
    """
    import re
    # Regular expression for validating an Email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)