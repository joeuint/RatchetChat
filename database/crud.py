from sqlalchemy.orm import Session
from uuid import uuid4
from . import models
import string
from secrets import SystemRandom
from argon2 import PasswordHasher

password_char_list = string.ascii_lowercase + string.ascii_uppercase + string.digits + '#$%&'

secure_rng = SystemRandom()

ph = PasswordHasher(
    hash_len=32,
    memory_cost=1024*1024,
    parallelism=4,
    time_cost=3,
)

def create_user(db: Session) -> tuple[str, int]:
    password = ''.join(secure_rng.choices(password_char_list, k=32))

    hashed_password = ph.hash(password)

    new_user = models.User(
        user_id = str(uuid4()),
        hashed_password = hashed_password,
    )

    db.add(new_user)
    db.commit()

    return password, new_user.user_id

def get_user_by_id(db: Session, user_id: str) -> models.User | None:
    return db.query(models.User).filter(models.User.user_id == user_id).one_or_none()

def new_convo_request(db: Session, target: models.User, requester: models.User) -> None:
    convo_request = models.ConvoRequest(
        convo_request_id = str(uuid4()),
        target_id = target.user_id,
        requester_id = requester.user_id,
    )

    db.add(convo_request)
    db.commit()

def get_convo_request_by_id(db: Session, convo_request_id: str) -> models.ConvoRequest | None:
    return db.query(models.ConvoRequest).filter(models.ConvoRequest.convo_request_id == convo_request_id).one_or_none()

def new_connection(db: Session, user1: models.User, user2: models.User):
    new_convo_connection = models.ConvoConnection(
        connection_id = str(uuid4()),
        user1 = user1.user_id,
        user2 = user2.user_id,
    )

    db.add(new_convo_connection)
    db.commit()

def authenticate_user(db: Session, user_id: str, password: str) -> models.User | None:
    user = db.query(models.User).filter(models.User.user_id == user_id ).one_or_none()

    if user is None:
        return None
    try:
        ph.verify(user.hashed_password, password)
    except:
        return None

    return user

def new_message(db: Session, connection: models.ConvoConnection, message: str):
    new_message = models.Message(
        id = str(uuid4()),
        connection_id = connection.connection_id,
        content = message
    )

    db.add(new_message)
    db.commit()
