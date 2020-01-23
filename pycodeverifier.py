import base64
import hashlib
import secrets
import json
import time
import jwt
import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup



random = secrets.token_bytes(64)
code_verifier = base64.b64encode(random, b'-_').decode().replace('=', '')

m = hashlib.sha256()
m.update(code_verifier.encode())
d = m.digest()
code_challenge = base64.b64encode(d, b'-_').decode().replace('=', '')


params = (
    ('response_type', 'code'),
    ('client_id', 'who-dis-auth-server'),
    ('code_challenge', code_challenge),
    ('code_challenge_method', 'S256'),
    ('redirect_url', 'https://www.google.com'),
)

response = requests.get('https://127.0.0.1:5001/auth', params=params, verify=False)
time.sleep(3)
print("Code challenge and Code Verifier obtained")
print("==============================")
time.sleep(3)
print("Requesting Authorization Code")
time.sleep(3)
Referer = "https://127.0.0.1:5001/auth?response_type=code&client_id=who-dis-auth-server&code_challenge="+code_challenge+"&code_challenge_method=S256&redirect_url=https://www.google.com"
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://127.0.0.1:5001',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Referer': Referer,
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

data = {
  'username': 'admin',
  'password': 'admin',
  'client_id': 'who-dis-auth-server',
  'redirect_url': 'https://www.google.com',
  'code_challenge': code_challenge
}

response = requests.post('https://127.0.0.1:5001/signin', headers=headers, data=data, verify=False)
interim=response.url.split('?')[1]
auth_code=interim.split('authorization_code=')[1]
time.sleep(3)
print("CODE_VERIFIER", code_verifier)
print("==============================")
print("AUTHORIZATION_CODE", auth_code)
time.sleep(3)
with open('privatecert.pem', 'rb') as file:
  private_key = file.read()

ISSUER = 'who-dis-auth-server'
CODE_LIFE_SPAN = 3600
JWT_LIFE_SPAN = 3600
payload = {
  "iss": ISSUER,
  "exp": time.time() + JWT_LIFE_SPAN
}

access_token = jwt.encode(payload, private_key, algorithm = 'RS256').decode()
print("==============================")
time.sleep(3)

print("ACCESS_TOKEN", access_token)
