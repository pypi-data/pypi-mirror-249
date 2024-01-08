import yaml
import hashlib
import requests

def passwordChecking(passwordInput,passwordTarget):
  hash_object   = hashlib.sha256()
  hash_object.update(passwordInput.encode())
  hash_password = hash_object.hexdigest()

  return hash_password==passwordTarget

def userAuthentication(user,passUser):
  global username
  global password
  global OCRLStatus
  global GAIStatus
 
  url               = f"https://storage.googleapis.com/devoteamlib/userAuthentication/{user}.yml"
  response          = requests.get(url, allow_redirects=True)
  content           = response.content.decode("utf-8")
  userInformation   = yaml.safe_load(content)

  try:
    if passwordChecking(passUser+user,userInformation['password']):
      username        = userInformation['username']
      password        = userInformation['password']
      OCRLStatus      = userInformation['OCRLayoutingStatus']
      GAIStatus       = userInformation['GenAIStatus']
      return "Authentication Success"

    else:
      return "Invalid password"

  except:
    return "Your username was not found"

def OCRLayoutingStatus(params):
  try:
    return params in OCRLStatus or 'All' in OCRLStatus
  except:
    return False

def GenAIStatus(params):
  try:
    return params in GAIStatus or 'All' in GAIStatus
  except:
    return False