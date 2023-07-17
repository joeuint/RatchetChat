import jwt
import os

if not os.path.exists('signingsecret.txt'):
    raise Exception('Please create a signingsecret.txt file in the auth folder and fill it with random characters.')

with open('sigingsecret.txt') as f:
    signing_secret = f.read()
    

def generate_jwt(user_id: int) -> str:
    token = jwt.encode({'user_id': user_id}, signing_secret, algorithm='HS512')

    return token