import bcrypt


def hash_password(password: str):
    bytes_password: bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes_password, salt)
    return hashed.decode()


def verify_password(password: str, hashed_pwd: bytes):
    return bcrypt.checkpw(
        current_password=password.encode(),
        hashed_password=hashed_pwd.encode(),
    )
