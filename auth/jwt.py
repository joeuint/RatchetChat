from fastapi import Request
import jwt
import os
from datetime import datetime
import time
from database import models, database

if not os.path.exists('./auth/signingsecret.txt'):
    raise Exception('Please create a signingsecret.txt file in the auth folder and fill it with random characters.')

with open('./auth/signingsecret.txt') as f:
    signing_secret = f.read()
    

def generate_jwt(user_id: int) -> str:
    token = jwt.encode({'user_id': user_id, 'exp': time.mktime(datetime.now().timetuple()) + 1209600}, signing_secret, algorithm='HS512')

    return token

def parse_token(token: str | None) -> str:
    if not isinstance(token, str):
        print('oh noeys')
        return ''
    else:
        split_token = token.split(' ')
        prefix = split_token[0]
        main_token = split_token[1]

        if prefix != 'Bearer':
            print('oh noes')
            return ''
        else: 
            return main_token


def verify_jwt(req: Request) -> models.User | None:
    try:
        payload: dict = jwt.decode(parse_token(req.headers.get('Authorization')), signing_secret, algorithms='HS512')
    except jwt.exceptions.InvalidTokenError:
        return None
    
    return database.SessionLocal().query(models.User).filter(models.User.user_id == payload.get('user_id')).one_or_none()