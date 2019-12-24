from cryptography.fernet import Fernet
x='uiVt5MjcLlSfwuhiQ29HPtAo30S_7eIkodPa-INcOOU='
def dec(token):
    f = Fernet(x)
    return f.decrypt(token)