import re

def getEmailDomain(email):
  try:
    return email.split('@')[1]
  except IndexError:
    raise ValueError('The provided email doesn\'t contain a domain')

def validateEmail(email):
  if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
    return True
  else:
    return False