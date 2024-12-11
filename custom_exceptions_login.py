#Custom exception if username or email is not found
class UserNotFound(Exception): pass

#Custom exception if username already exists
class UserExists(Exception): pass

#Incorrect login credentials
class UnauthorizedLogin(Exception): pass

#Tracker was not found in the database
class TrackerDNE(Exception): pass

#Use a new value for the user setting trying to be changed
class UnauthorizedUpdate(Exception): pass