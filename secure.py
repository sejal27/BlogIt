import random
import hashlib
import hmac
from string import letters

"""
Functions to make secure hash of user id cookie
Secret - Random string, normally not stored in the code.
Generlly stored in a module that's only on the production machine.
"""
secret = "iamnosecret"

# Takes a string as an input and returns the secured value, using secret string and HMAC.
def make_secure_val(s):
  return "%s|%s" % (s, hmac.new(secret, s).hexdigest())

# Takes a string that contains the hash as input. Splits it into two.
#Uses the make_secure_val function to check if the secured value of the string matches the value in the hash.
def check_secure_val(s):
    val=s.split('|')[0]
    if s==make_secure_val(val):
        return val

#Generate Salt - a random character string
def make_salt(length=5):
  return ''.join(random.choice(letters) for i in xrange(length))

# Generats the password hash using sha256 and returns salt and hash value of passwrd.
def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

# Checks if the password is valid by comparing the hashed values
def valid_pw(name, pw, h):
    salt=h.split(',')[0]
    return h == make_pw_hash(name,pw,salt)