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
        requester_id = target.user_id,
        target_id = requester.user_id,
    )

    db.add(convo_request)
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