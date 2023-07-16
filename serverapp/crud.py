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