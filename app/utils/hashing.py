import bcrypt

def hash_password(password: str) -> str:
    # Hash the password
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verify if the plain password matches the hashed one
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
