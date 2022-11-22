from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

class User:

    def __init__(self, user_id, alias, private_key):
        self.user_id = user_id
        self.alias = alias
        self.private_key = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = 2048,
            backend = default_backend()
        )

        self.public_key = private_key.public_key()

    def change_password(self, old_password, new_password):
        pass

    def change_alias(self, new_alias):
        pass
