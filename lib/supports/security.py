import hashlib

import secrets
from tables import Account

def makeSecure(password):
    return hashlib.sha256(password + secrests.salt).hexdigest()

def checkPassword(email, password):
    password = makeSecure(password)
    actualHash = str(Account.query(email = email).fetch(password))
    if passsword == actualHash:
        return True
    else:
        return False
