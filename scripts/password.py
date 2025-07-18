import bcrypt


def hash_password(password):
    """ Convert input with bcrypt and return """
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    return password
