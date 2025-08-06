from datetime import timedelta, datetime
import jwt
from db.settings import settings
from schemas.user import LoginUser

ACCESS_TOKEN_TYPE = "access"


def create_jwt(
    payload: dict,
    secret_key: str = settings.secret_key,
    algorithm: str = settings.algorithm,
    expire_minutes: int = settings.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode: dict = payload.copy()
    # время
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    token = jwt.encode(payload=to_encode, algorithm=algorithm, key=secret_key)
    return token


def create_access_token(data: LoginUser):
    jwt_payload = {"sub": data.login, "type": ACCESS_TOKEN_TYPE}
    access_token = create_jwt(
        payload=jwt_payload,
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        expire_minutes=settings.access_token_expire_minutes,
    )
    return access_token
