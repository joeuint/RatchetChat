from fastapi import FastAPI, Depends

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption, PublicFormat

from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models
from . import crud

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

@app.post('/accountcreate')
def gen_account(db: Session = Depends(get_db)):
    unhashed, user_id = crud.create_user(db)
    return {
                'id': user_id,
                'password': unhashed,
            }