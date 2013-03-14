import logging
import re
import hmac
import random
import string
import hashlib
import time
from google.appengine.api import memcache
		

# Implement the hash_str function to use HMAC and our SECRET instead of md5
SECRET = 'imsosecret'

def is_valid_username(username):
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	return USER_RE.match(username)

def is_valid_password(password):
	USER_RE = re.compile(r"^.{3,20}$")
	return USER_RE.match(password)

def verify_password(password,verify):
	return (password==verify)

def is_valid_email(email):
	USER_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
	return USER_RE.match(email)
	
def hash_str(s):
	###Your code here
	return hmac.new(SECRET,s).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s,hash_str(s))

def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val

def make_salt():
	return ''.join(random.choice(string.letters) for x in xrange(5))

# Implement the function valid_pw() that returns True if a user's password 
# matches its hash. You will need to modify make_pw_hash.

def make_pw_hash(name, pw, salt=""):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
	value = h.split(",")
	salt = value[1]
	return value[0] == hashlib.sha256(name + pw + salt).hexdigest()
	
def flushCache():
	memcache.flush_all()
	self.redirect("/")

def time_lapse(timestamp):
	timenow = int(time.time())
	delta = timenow - timestamp

	minute = 60
	hour = minute*60
	day = (hour*24)
	week = (day*7)

	if delta < 60:
		return "seconds"
	elif delta/minute < 60:
		return "%s minutes ago" %(delta/minute)
	elif delta/hour < 24:
		return "%s hours ago" %(delta/hour)
	elif delta/day < 7:
		return "%s days ago" %(delta/day)
	else:
		return "%s weeks ago" %(delta/week)
