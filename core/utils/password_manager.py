from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def has_password(plain_password: str) -> str:
    hashed_password = pwd_context.hash(plain_password)
    return hashed_password

def verify_password(raw_password: str, hashed_password: str) -> bool:
    is_valid = pwd_context.verify(raw_password, hashed_password)
    return is_valid