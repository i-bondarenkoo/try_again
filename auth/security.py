import bcrypt


def hash_password(current_password: str):
    bytes_password: bytes = current_password.encode()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes_password, salt)
    return hashed_password.decode()


def verify_password(current_password: str, hashed_password: bytes):
    return bcrypt.checkpw(
        current_password=current_password.encode(),
        hashed_password=hashed_password.encode(),
    )
