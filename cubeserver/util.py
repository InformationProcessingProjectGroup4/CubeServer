from bcrypt import gensalt, hashpw, checkpw
    
def hash_password(password: str) -> str:
    hash = hashpw(password.encode("utf-8"), gensalt(10))
    hash = hash.decode("utf-8")
    return hash

def check_password(password: str, hash: str) -> bool:
    same = checkpw(password.encode("utf-8"), hash.encode("utf-8"))
    return same
