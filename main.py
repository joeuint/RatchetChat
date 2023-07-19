from fastapi import FastAPI, Depends, Request, Response, status, Body
from sqlalchemy import delete

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption, PublicFormat

from sqlalchemy.orm import Session

from database.database import SessionLocal, engine
from database import models
from database import crud

from auth import jwt

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/crypto/genkeypair')
def gen_keys():
    priv_key = X25519PrivateKey.generate()

    print(priv_key.private_bytes_raw())
    
    return {
                'private': priv_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()),
                'public': priv_key.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
            }

@app.post('/token')
def get_jwt(response: Response, body: dict = Body(...),  db: Session = Depends(get_db)):
    user_id = body.get('user_id')
    password = body.get('password')

    if user_id is None or password is None:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return 'user_id or password is empty'

    if crud.authenticate_user(db, user_id, password):
        return { 'token': jwt.generate_jwt(user_id) }
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return 'Incorrect Credentials'

@app.post('/accountcreate')
def gen_account(db: Session = Depends(get_db)):
    unhashed, user_id = crud.create_user(db)
    return {
                'id': user_id,
                'password': unhashed,
            }

@app.post('/startconvo/{user_id}')
def start_convo(response: Response, request: Request, user_id: str, db: Session = Depends(get_db)):
    sender_user = jwt.verify_jwt(request)

    if sender_user is None:
        response.status_code = status.HTTP_403_FORBIDDEN
        return 'Auth Failed'

    target_user = crud.get_user_by_id(db, user_id)

    if target_user is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return 'User Not Found'
    
    crud.new_convo_request(db, target_user, sender_user)

@app.post('/acceptconvo/{convo_id}')
def accept_convo(convo_id: str, request: Request, response: Response, db: Session = Depends(get_db)):
    accepter_user = jwt.verify_jwt(request)

    if accepter_user is None:
        response.status_code = status.HTTP_403_FORBIDDEN
        return 'Auth Failed'

    convo_request = crud.get_convo_request_by_id(db, convo_id)

    if convo_request is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return 'Convo Request not found'

    if accepter_user.user_id != convo_request.target_id:
        response.status_code = status.HTTP_403_FORBIDDEN
        return 'Not Authorized'

    crud.new_connection(db, accepter_user, crud.get_user_by_id(db, convo_request.requester_id))

    db.delete(convo_request)

    db.commit()
