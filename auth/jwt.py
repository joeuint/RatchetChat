import jwt
import os
from datetime import datetime
import time

if not os.path.exists('signingsecret.txt'):
    raise Exception('Please create a signingsecret.txt file in the auth folder and fill it with random characters.')

with open('sigingsecret.txt') as f:
    signing_secret = f.read()
    

def generate_jwt(user_id: int) -> str:
    token = jwt.encode({'user_id': user_id, 'exp': time.mktime(datetime.now().timetuple()) + 1209600}, signing_secret, algorithm='HS512')

    return token