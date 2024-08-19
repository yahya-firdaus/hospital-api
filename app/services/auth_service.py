from flask_bcrypt import (check_password_hash,
                          generate_password_hash)

def hash_password(password):
    return generate_password_hash(password).decode('utf-8')

def check_password(plain_password, hashed_password):
    return check_password_hash(plain_password, hashed_password)