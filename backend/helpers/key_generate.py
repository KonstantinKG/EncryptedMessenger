from cryptography.fernet import Fernet


class KeyGenerator:
    def __init__(self):
        self.key = Fernet.generate_key()