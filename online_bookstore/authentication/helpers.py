import re

def email_validator(email):
    import re
    pattern = r'^[\w\.-]+(\+[\w\.-]+)?@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

def password_validator(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?`~]', password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True
