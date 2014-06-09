import os

DEBUG = os.environ.get('DEBUG', False) == "1"
SECRET_KEY = os.environ.get('SECRECT',"notsecret")
AUTH_TOKEN_KEY = os.environ.get('AUTH_KEY',"deterministic")

USERNAME = os.environ.get('USERNAME',None)
PASSWORD = os.environ.get('PASSWORD',None)
